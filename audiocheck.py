#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyaudio
def audiocheck():
    po = pyaudio.PyAudio()
    for index in range(po.get_device_count()):
        desc = po.get_device_info_by_index(index)
        print("DEVICE: %s  INDEX:  %s  RATE:  %s " % (desc["name"], index, int(desc["defaultSampleRate"])))

    #if desc["name"] == "record":
    #

if __name__ == '__main__':
    audiocheck()