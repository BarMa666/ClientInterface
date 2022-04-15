USE incoming_data;

CREATE TABLE data_source(
    id integer NOT NULL AUTO_INCREMENT,
    source_name varchar(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id)
    );

CREATE TABLE data_field(
    id integer NOT NULL AUTO_INCREMENT,
    field_name varchar(50) NOT NULL,
    source_id integer NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (source_id) REFERENCES data_source(id),
    UNIQUE (id)
    );

CREATE TABLE data_main(
    id integer NOT NULL AUTO_INCREMENT,
    field_id integer NOT NULL,
    field_value decimal(12, 2) NULL,
    date datetime NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (field_id) REFERENCES data_field(id),
    UNIQUE (id)
    );
