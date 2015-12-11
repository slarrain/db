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

CREATE TABLE compensation (
  COMPENSATION_ID           INTEGER   PRIMARY KEY,
  LOBBYIST_ID               INTEGER,
  COMPENSATION_AMOUNT       VARCHAR,
  CLIENT_ID                 INTEGER
);

CREATE TABLE employer (
  EMPLOYER_ID   INTEGER   PRIMARY KEY,
  NAME          VARCHAR,
  ADDRESS_1     VARCHAR,
  ADDRESS_2     VARCHAR,
  CITY          VARCHAR,
  STATE         VARCHAR,
  ZIP           INTEGER
);

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

CREATE TABLE activity (
  LOBBYING_ACTIVITY_ID      INTEGER   PRIMARY KEY,
  ACTION_SOUGHT             VARCHAR,
  DEPARTMENT                VARCHAR,
  CLIENT_ID                 INTEGER,
  LOBBYIST_ID               INTEGER
);

CREATE TABLE lobbyist (
  LOBBYIST_ID               INTEGER,
  LOBBYIST_SALUTATION       VARCHAR,
  LOBBYIST_FIRST_NAME       VARCHAR,
  LOBBYIST_LAST_NAME        VARCHAR
);

CREATE TABLE connection (
  LOBBYIST_ID               INTEGER,
  EMPLOYER_ID               INTEGER,
  CLIENT_ID                 INTEGER
);
