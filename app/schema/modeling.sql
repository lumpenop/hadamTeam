CREATE TABLE common
(
	common_id            INTEGER NOT NULL,
	parent_code          VARCHAR(20) NULL,
	code                 VARCHAR(20) NULL,
	create_date          VARCHAR(20) NULL,
	update_date          VARCHAR(20) NULL,
	code_name            VARCHAR(20) NULL
);



ALTER TABLE common
ADD PRIMARY KEY (common_id);



CREATE TABLE files
(
	file_id              INTEGER NOT NULL,
	file_name            VARCHAR(20) NULL,
	file_path            VARCHAR(20) NULL,
	create_date          VARCHAR(20) NULL,
	update_date          VARCHAR(20) NULL
);



ALTER TABLE files
ADD PRIMARY KEY (file_id);



CREATE TABLE member
(
	member_id            INTEGER NOT NULL,
	name                 VARCHAR(20) NULL,
	age                  INTEGER NULL,
	sex                  VARCHAR(20) NULL,
	create_date          VARCHAR(20) NULL,
	update_date          VARCHAR(20) NULL,
	file_id              INTEGER NULL
);



ALTER TABLE member
ADD PRIMARY KEY (member_id);



CREATE TABLE payment
(
	payment_id           INTEGER NOT NULL,
	payment_price        INTEGER NULL,
	total_price          INTEGER NULL,
	cencel_price         INTEGER NULL,
	create_date          VARCHAR(20) NULL,
	update_date          VARCHAR(20) NULL,
	price_id             INTEGER NULL,
	member_id            INTEGER NULL
);



ALTER TABLE payment
ADD PRIMARY KEY (payment_id);



CREATE TABLE price
(
	price_id             INTEGER NOT NULL,
	size                 VARCHAR(20) NULL,
	price_name           VARCHAR(20) NULL,
	price                INTEGER NULL,
	classification       VARCHAR(20) NULL,
	create_date          VARCHAR(20) NULL,
	update_date          VARCHAR(20) NULL
);



ALTER TABLE price
ADD PRIMARY KEY (price_id);



ALTER TABLE member
ADD FOREIGN KEY R_15 (file_id) REFERENCES files (file_id);



ALTER TABLE payment
ADD FOREIGN KEY R_10 (price_id) REFERENCES price (price_id);



ALTER TABLE payment
ADD FOREIGN KEY R_11 (member_id) REFERENCES member (member_id);


