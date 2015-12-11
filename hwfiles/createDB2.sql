DROP DATABASE IF EXISTS lobbydb;
CREATE DATABASE lobbydb;
\connect lobbydb

CREATE TABLE client (
    CLIENT_ID     INTEGER   PRIMARY KEY,
    NAME          VARCHAR,
    ADDRESS_1     VARCHAR,
    ADDRESS_2     VARCHAR,
    CITY          VARCHAR,
    STATE         VARCHAR,
    ZIP           VARCHAR
);

CREATE INDEX name_idx ON client (NAME);

CREATE TABLE compensation (
  COMPENSATION_ID           INTEGER   PRIMARY KEY,
  LOBBYIST_ID               INTEGER,
  COMPENSATION_AMOUNT       numeric,
  CLIENT_ID                 INTEGER REFERENCES client (CLIENT_ID)
);

CREATE INDEX lobbyist_idx ON compensation (LOBBYIST_ID);

CREATE TABLE employer (
  EMPLOYER_ID   INTEGER   PRIMARY KEY,
  NAME          VARCHAR,
  ADDRESS_1     VARCHAR,
  ADDRESS_2     VARCHAR,
  CITY          VARCHAR,
  STATE         VARCHAR,
  ZIP           VARCHAR
);

CREATE  INDEX emp_name_idx ON employer (NAME);

CREATE TABLE expenditures (
  EXPENDITURE_ID            INTEGER   PRIMARY KEY,
  LOBBYIST_ID               INTEGER,
  ACTION                    VARCHAR,
  AMOUNT                    numeric,
  EXPENDITURE_DATE          DATE,
  PURPOSE                   VARCHAR,
  RECIPIENT                 VARCHAR,
  CLIENT_ID                 INTEGER REFERENCES client (CLIENT_ID)
);

CREATE INDEX lobbyist_exp_idx ON expenditures (LOBBYIST_ID);

CREATE TABLE activity (
  LOBBYING_ACTIVITY_ID      INTEGER   PRIMARY KEY,
  ACTION_SOUGHT             VARCHAR,
  DEPARTMENT                VARCHAR,
  CLIENT_ID                 INTEGER REFERENCES client (CLIENT_ID),
  LOBBYIST_ID               INTEGER
);

CREATE INDEX client_act_idx ON activity (CLIENT_ID);
CREATE INDEX lobbyist_act_idx ON activity (LOBBYIST_ID);

CREATE TABLE lobbyist (
  LOBBYIST_ID               INTEGER PRIMARY KEY,
  LOBBYIST_SALUTATION       VARCHAR,
  LOBBYIST_FIRST_NAME       VARCHAR,
  LOBBYIST_LAST_NAME        VARCHAR
);

CREATE  INDEX lob_fname_idx ON lobbyist (LOBBYIST_FIRST_NAME);
CREATE  INDEX lob_lname_idx ON lobbyist (LOBBYIST_LAST_NAME);

CREATE TABLE connection (
  LOBBYIST_ID               INTEGER REFERENCES lobbyist (LOBBYIST_ID),
  EMPLOYER_ID               INTEGER REFERENCES employer (EMPLOYER_ID,
  CLIENT_ID                 INTEGER REFERENCES client (CLIENT_ID),
  PRIMARY KEY (LOBBYIST_ID,EMPLOYER_ID,CLIENT_ID)
);
