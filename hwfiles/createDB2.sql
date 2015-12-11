CREATE DATABASE lobbydb;

CREATE TABLE client (
    CLIENT_ID     INTEGER   PRIMARY KEY,
    NAME          VARCHAR,
    ADDRESS_1     VARCHAR,
    ADDRESS_2     VARCHAR,
    CITY          VARCHAR,
    STATE         VARCHAR,
    ZIP           INTEGER
);

CREATE INDEX name_idx ON client (NAME);

CREATE TABLE compensation (
  COMPENSATION_ID           INTEGER   PRIMARY KEY,
  LOBBYIST_ID               INTEGER,
  COMPENSATION_AMOUNT       VARCHAR,
  CLIENT_ID                 INTEGER
);

CREATE INDEX lobbyist_idx ON compensation (LOBBYIST_ID);

CREATE TABLE employer (
  EMPLOYER_ID   INTEGER   PRIMARY KEY,
  NAME          VARCHAR,
  ADDRESS_1     VARCHAR,
  ADDRESS_2     VARCHAR,
  CITY          VARCHAR,
  STATE         VARCHAR,
  ZIP           INTEGER
);

CREATE  INDEX emp_name_idx ON employer (NAME);

CREATE TABLE expenditures (
  EXPENDITURE_ID            INTEGER   PRIMARY KEY,
  LOBBYIST_ID               INTEGER,
  ACTION                    VARCHAR,
  AMOUNT                    VARCHAR,
  EXPENDITURE_DATE          DATE,
  PURPOSE                   VARCHAR,
  RECIPIENT                 VARCHAR,
  CLIENT_ID                 INTEGER
);

CREATE INDEX lobbyist_exp_idx ON expenditures (LOBBYIST_ID);

CREATE TABLE activity (
  LOBBYING_ACTIVITY_ID      INTEGER   PRIMARY KEY,
  ACTION_SOUGHT             VARCHAR,
  DEPARTMENT                VARCHAR,
  CLIENT_ID                 INTEGER,
  LOBBYIST_ID               INTEGER
);

CREATE INDEX client_act_idx ON activity (CLIENT_ID);
CREATE INDEX lobbyist_act_idx ON activity (LOBBYIST_ID);

CREATE TABLE lobbyist (
  LOBBYIST_ID               INTEGER,
  EMPLOYER_ID               INTEGER,
  CLIENT_ID                 INTEGER,
  LOBBYIST_SALUTATION       VARCHAR,
  LOBBYIST_FIRST_NAME       VARCHAR,
  LOBBYIST_LAST_NAME        VARCHAR
);

CREATE UNIQUE INDEX lobbyist_employer_client_idx ON activity (LOBBYIST_ID,EMPLOYER_ID,CLIENT_ID);