DROP DATABASE auscats;
CREATE DATABASE auscats;
USE auscats;
CREATE TABLE ORG_UNITS (UNIT_ID INT(5) UNSIGNED NOT NULL,
    UNIT_NAME VARCHAR(100),
    PRIMARY KEY (UNIT_ID));

CREATE TABLE ADMIN (USER_ID VARCHAR(8) NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    UNIT_ID INT(5) UNSIGNED NOT NULL,
    PRIMARY KEY (USER_ID),
    FOREIGN KEY (UNIT_ID) REFERENCES ORG_UNITS (UNIT_ID) 
    ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE ADMIN_PERM (USER_ID VARCHAR(8) NOT NULL,
    PERMISSION VARCHAR(50) NOT NULL);

CREATE TABLE MODULES (MODULE_ID INT(6) UNSIGNED NOT NULL AUTO_INCREMENT, 
    STATUS VARCHAR(10) NOT NULL,
    NAME VARCHAR(50) NOT NULL, 
    BLURB VARCHAR(500) NOT NULL, 
    NUM_QUESTIONS INT(2) UNSIGNED NOT NULL,
    PRIMARY KEY(MODULE_ID), 
    UNIQUE KEY module (NAME));

CREATE TABLE MODULE_CONTENT (MODULE_ID INT(6) UNSIGNED NOT NULL, 
    REVISION INT(6) UNSIGNED NOT NULL, 
    CONTENT BLOB, 
    EDITOR VARCHAR(8) NOT NULL, 
    TIME_CREATED DATETIME NOT NULL DEFAULT NOW(),
    FOREIGN KEY (MODULE_ID) REFERENCES MODULES (MODULE_ID)
    ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (EDITOR) REFERENCES ADMIN (USER_ID) 
    ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE QUIZ_QUESTIONS (MODULE_ID INT(6) UNSIGNED NOT NULL,
    QUESTION_ID INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,
    QUESTION VARCHAR(200) NOT NULL, 
    PRIMARY KEY(QUESTION_ID),
    FOREIGN KEY (MODULE_ID) REFERENCES MODULES (MODULE_ID) 
    ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE QUIZ_ANSWERS (QUESTION_ID INT(6) UNSIGNED NOT NULL,
    ANSWER_ID INT(6) UNSIGNED NOT NULL AUTO_INCREMENT,
    ANSWER VARCHAR(200) NOT NULL,
    PRIMARY KEY(ANSWER_ID),
    FOREIGN KEY (QUESTION_ID) REFERENCES QUIZ_QUESTIONS (QUESTION_ID)
    ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE CORRECT_ANSWERS (QUESTION_ID INT(6) UNSIGNED NOT NULL,
    ANSWER_ID INT(6) UNSIGNED NOT NULL,
    FOREIGN KEY (QUESTION_ID) REFERENCES QUIZ_QUESTIONS (QUESTION_ID)
    ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (ANSWER_ID) REFERENCES QUIZ_ANSWERS (ANSWER_ID)
    ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE USER_PROGRESS (USER_ID VARCHAR(8) NOT NULL,
    MODULE_ID INT(6) UNSIGNED NOT NULL,
    LAST_VIEWED INT(2) UNSIGNED NOT NULL,
    FOREIGN KEY (MODULE_ID) REFERENCES MODULES (MODULE_ID)
    ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE TABLE GRADEBOOK (USER_ID VARCHAR (8) NOT NULL,
    ORG_UNIT VARCHAR(50) NOT NULL,
    QUESTION_ID INT(6) UNSIGNED NOT NULL,
    ANSWER_ID INT(6) UNSIGNED NOT NULL,
    FOREIGN KEY (QUESTION_ID) REFERENCES QUIZ_QUESTIONS (QUESTION_ID)
    ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (ANSWER_ID) REFERENCES QUIZ_ANSWERS (ANSWER_ID)
    ON UPDATE NO ACTION ON DELETE NO ACTION);

CREATE VIEW vw_USER_ANSWERS AS
    select USER_ID, ORG_UNIT, q.MODULE_ID, g.QUESTION_ID, g.ANSWER_ID
    FROM GRADEBOOK g, QUIZ_QUESTIONS q 
    WHERE g.QUESTION_ID = q.QUESTION_ID 
    ORDER BY USER_ID, MODULE_ID, QUESTION_ID;

CREATE VIEW vw_USER_CORRECT_ANSWERS AS
    select *
    FROM vw_USER_ANSWERS
    WHERE ANSWER_ID IN (SELECT ANSWER_ID from CORRECT_ANSWERS)
    ORDER BY USER_ID, MODULE_ID, QUESTION_ID;

CREATE VIEW vw_TOTAL_ATTEMPTS_PER_QUESTION AS
    SELECT QUESTION_ID, COUNT(*) AS TOTAL_ATTEMPTS FROM
    GRADEBOOK
    WHERE QUESTION_ID IN (SELECT QUESTION_ID FROM QUIZ_QUESTIONS)
    GROUP BY QUESTION_ID;

CREATE VIEW vw_TOTAL_CORRECT_PER_QUESTION AS
    SELECT QUESTION_ID, COUNT(*) AS CORRECT_ATTEMPTS FROM
    vw_USER_CORRECT_ANSWERS
    WHERE QUESTION_ID IN (SELECT QUESTION_ID FROM QUIZ_QUESTIONS)
    GROUP BY QUESTION_ID;

CREATE VIEW vw_QUESTION_STATISTICS AS
    SELECT MODULE_ID, q.QUESTION_ID, TOTAL_ATTEMPTS, CORRECT_ATTEMPTS,
    (CORRECT_ATTEMPTS/TOTAL_ATTEMPTS * 100) AS PERCENT_SUCCESS
    FROM QUIZ_QUESTIONS q, vw_TOTAL_ATTEMPTS_PER_QUESTION t, vw_TOTAL_CORRECT_PER_QUESTION c
    WHERE q.QUESTION_ID = t.QUESTION_ID
    AND q.QUESTION_ID = c.QUESTION_ID
    ORDER BY MODULE_ID, QUESTION_ID;

CREATE VIEW vw_LAST_UPDATED_MODULE AS
    SELECT MODULE_ID, EDITOR, TIME_CREATED as LAST_UPDATED
    FROM MODULE_CONTENT 
    WHERE TIME_CREATED IN 
    (SELECT MAX(TIME_CREATED) FROM MODULE_CONTENT GROUP BY MODULE_ID);

CREATE VIEW vw_ADMIN_MODULE_INFO AS
    select m.MODULE_ID, m.NAME, m.STATUS, l.EDITOR, l.LAST_UPDATED
    FROM MODULES m, vw_LAST_UPDATED_MODULE l
    WHERE m.MODULE_ID = l.MODULE_ID
    ORDER BY MODULE_ID, LAST_UPDATED;
