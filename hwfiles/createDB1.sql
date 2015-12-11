DROP DATABASE IF EXISTS lobbydb;
CREATE DATABASE lobbydb;
\connect lobbydb

CREATE TABLE client (
    CLIENT_ID     NUMERIC   PRIMARY KEY,
    NAME          VARCHAR,
    ADDRESS_1     VARCHAR,
    ADDRESS_2     VARCHAR,
    CITY          VARCHAR,
    STATE         VARCHAR,
    ZIP           VARCHAR
);

CREATE TABLE compensation (
  COMPENSATION_ID           NUMERIC   PRIMARY KEY,
  LOBBYIST_ID               NUMERIC,
  COMPENSATION_AMOUNT       NUMERIC,
  CLIENT_ID                 NUMERIC
);

CREATE TABLE employer (
  EMPLOYER_ID   NUMERIC   PRIMARY KEY,
  NAME          VARCHAR,
  ADDRESS_1     VARCHAR,
  ADDRESS_2     VARCHAR,
  CITY          VARCHAR,
  STATE         VARCHAR,
  ZIP           VARCHAR
);

CREATE TABLE expenditures (
  EXPENDITURE_ID            NUMERIC   PRIMARY KEY,
  LOBBYIST_ID               NUMERIC,
  ACTION                    VARCHAR,
  AMOUNT                    numeric,
  EXPENDITURE_DATE          DATE,
  PURPOSE                   VARCHAR,
  RECIPIENT                 VARCHAR,
  CLIENT_ID                 NUMERIC
);

CREATE TABLE activity (
  LOBBYING_ACTIVITY_ID      NUMERIC   PRIMARY KEY,
  ACTION_SOUGHT             VARCHAR,
  DEPARTMENT                VARCHAR,
  CLIENT_ID                 NUMERIC,
  LOBBYIST_ID               NUMERIC
);

CREATE TABLE lobbyist (
  LOBBYIST_ID               NUMERIC   PRIMARY KEY,
  LOBBYIST_SALUTATION       VARCHAR,
  LOBBYIST_FIRST_NAME       VARCHAR,
  LOBBYIST_LAST_NAME        VARCHAR
);

CREATE TABLE connection (
  LOBBYIST_ID               NUMERIC,
  EMPLOYER_ID               NUMERIC,
  CLIENT_ID                 NUMERIC
);
