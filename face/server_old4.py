from flask import Flask, render_template, request
import numpy as np
import json

import base64
import cv2
import os

from facenet_pytorch import MTCNN as FastMTCNN
import tensorflow as tf

from numpy import expand_dims
from numpy import asarray
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
from keras_vggface.utils import decode_predictions

import torch

from PIL import Image
from scipy.spatial.distance import cosine

def box_sort_index(boxes):
    area = np.array([(x2-x1) * (y2-y1) for x1,y1,x2,y2 in boxes])
    return np.argsort(area)[::-1]

def check_coord(range, coord):
    if coord < 0:
        return 0
    elif coord >= range:
        return range - 1
    else:
        return coord

def extract_face2(detector, pixels, required_size=(224, 224)):
    image = Image.fromarray(pixels)
    boxes, _ = detector.detect(image)

    if boxes is None:
        print('No face!')
        return None,None

    faces, r_boxes = [], []
    for i, result in enumerate(boxes):
        result = result.tolist()
        # print(result)
        x_range, y_range = pixels.shape[1], pixels.shape[0]
        x1, y1, x2, y2 = check_coord(x_range, int(result[0])), check_coord(y_range, int(result[1])), \
                         check_coord(x_range, int(result[2])), check_coord(y_range, int(result[3]))

        print('face coord:', x1, ',', y1,',', x2, ',', y2, ' shape:', pixels.shape)
        face = pixels[y1:y2, x1:x2].copy()
        # print('face type:', type(face), ' shape : ', face.shape)

        image_face = Image.fromarray(face)
        image_face = image_face.resize(required_size)
        face_array = asarray(image_face)
        # print('face_array type:', type(face_array))  # , ' shape :', face_array.shape)
        part_pixels = face_array.astype('float32')
        samples = expand_dims(part_pixels, axis=0)
        samples = preprocess_input(samples, version=2)

        # print("loop:", i)
        faces.append(samples)
        r_boxes.append((x1, y1, x2, y2))
        # return samples
    return faces, r_boxes


def make_embedding_vector(pixels, detector, face_recognizer):
    face, boxes = extract_face2(detector, pixels)

    if face is None or len(face) == 0:
        return None, None, None

    boxes_indexes = box_sort_index(boxes)
    embedding_vector = face_recognizer.predict(face[boxes_indexes[0]])
    return embedding_vector, face[boxes_indexes[0]], boxes[boxes_indexes[0]]


def make_embedding_vector_file_from_file(file_name, detector, face_recognizer, target_dir):
    pixels = cv2.imread(file_name)
    pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)

    embedding_vector, _, _ = make_embedding_vector(pixels, detector, face_recognizer)
    if embedding_vector is None:
        return None

    only_file_name = os.path.basename(file_name)
    only_file_name, _ = os.path.splitext(only_file_name)

    save_path = os.path.join(target_dir, only_file_name + '.npy')
    # print('save_path:', save_path)
    np.save(save_path, embedding_vector)
    return embedding_vector

def make_embedding_vector_file_from_dir(detector, face_recognizer, read_dir, target_dir):
    for file_name in os.listdir(read_dir):
        #print(file_name)
        read_file_name = os.path.join(read_dir, file_name)
        #print('read_file_name:',read_file_name)
        make_embedding_vector_file_from_file(read_file_name, detector, face_recognizer, target_dir)


def make_embedding_vector_dict_from_dir(dir_name):
    result_dict = {}

    for file_name in os.listdir(dir_name):
        # print(file_name)
        if file_name.endswith('.npy'):
            embedding_vector = np.load(os.path.join(dir_name, file_name))
            only_file_name, _ = os.path.splitext(file_name)
            result_dict[only_file_name] = embedding_vector
    return result_dict

def find_face(embedding_vector, embedding_dict, thresh = 0.5):
    for key, value in embedding_dict.items():
        #print('find_face:', type(embedding_vector),',',print(value), ',', type(value))
        score = cosine(embedding_vector, value)
        if score <= thresh:
            return key # Match
            #print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
    return 'Unknown'

def predict_face_from_frame(frame, face_dict, detector, face_recognizer):
    embedding_vector, _, box = make_embedding_vector(frame, detector, face_recognizer)
    if embedding_vector is not None:
        return find_face(embedding_vector, face_dict), box
    else:
        return None, None

#return embedding_vector, face, NoFace, duplicated
def crop_face(frame, face_dict, detector, face_recognizer):
    embedding_vector, face, _ = make_embedding_vector(frame, detector, face_recognizer)
    if embedding_vector is None:
        return None,None, True, False
    else:
        r = find_face(embedding_vector, embedding_vector_dict)
        if r != 'Unkown':
            return embedding_vector, face, False, False
        else:
            return None, None, False, True

def predict_face_from_file(file_name, face_dict, detector, face_recognizer):
    pixels = cv2.imread(file_name)
    pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)
    return predict_face_from_frame(pixels, face_dict, detector, face_recognizer)

def predict_class_face_from_file(file_name, detector, face_recognizer):
    results = []

    pixels = cv2.imread(file_name)
    pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)

    faces, boxes = extract_face2(detector, pixels)
    if faces is None or len(faces) == 0:
        return None

    boxes = box_sort_index(boxes)
    yhat = face_recognizer.predict(faces[boxes[0]])
    results.append(decode_predictions(yhat))

    return results

def decode_image(data):
    decode_bytes = data.encode('ascii')
    decode_bytes = base64.b64decode(decode_bytes)
    decode_bytes = np.frombuffer(decode_bytes, dtype=np.int8)  # np.frombytes(decode_bytes)
    decode_img = cv2.imdecode(decode_bytes, cv2.IMREAD_COLOR)

    return decode_img
app = Flask(__name__)

@app.route('/transfer_image', methods=['POST'])
def face_recognizer():
    if request.method == 'POST':
        params = json.loads(request.get_data(), encoding='utf-8')
        decode_img = decode_image(params['frame'])
        outtext, box = predict_face_from_frame(decode_img, embedding_vector_dict, fast_mtcnn, model_embedding)
        print(outtext)

        response = {}
        if outtext is None:
            response['no_face'] = True
            response['message'] = 'No Face!'
        else:
            print(box)
            response['no_face'] = False
            response['message'] = outtext
            response['box'] = box

        return json.dumps(response, indent=4, ensure_ascii=True)

@app.route('/register_face', methods=['POST'])
def register_face():
    if request.method == 'POST':
        params = json.loads(request.get_data(), encoding='utf-8')

        error_code = 0
        params['name'] = params['name'].strip()

        if params['name'] == '':
          error_code = -1
        elif params['name'] in embedding_vector_dict:
            error_code = -2
        else:
            decode_img = decode_image(params['frame'])
            embedding_vector, face, no_face, duplicated = crop_face(decode_img, embedding_vector_dict, fast_mtcnn, model_embedding)
            if no_face:
                error_code = -3
            elif duplicated:
                error_code = -4
            else:
                cv2.cvtColor(decode_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite('register_person/' + params['name'] + '.jpg', cv2.cvtColor(decode_img, cv2.COLOR_RGB2BGR))
                np.save('register_person_numpy/' + params['name'] + '.npy', embedding_vector)
                embedding_vector_dict[params['name']] = embedding_vector

        response = {}
        response['error_code'] = error_code
        return json.dumps(response, indent=4, ensure_ascii=True)

if __name__ == '__main__':
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    fast_mtcnn = FastMTCNN(keep_all=True, device=device)

    '''
    from tensorflow.compat.v1 import ConfigProto
    from tensorflow.compat.v1 import InteractiveSession

    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config) '''
    
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    print(device)
    model_embedding = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    model = VGGFace(model='resnet50')
    make_embedding_vector_file_from_dir(fast_mtcnn, model_embedding, 'register_person', 'register_person_numpy')
    embedding_vector_dict = make_embedding_vector_dict_from_dir('register_person_numpy')

    outtext = 'outtext'
    app.run(host='0.0.0.0', port=1234, debug=False)
