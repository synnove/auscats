SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE ORG_UNITS;
TRUNCATE TABLE ADMIN;
TRUNCATE TABLE ADMIN_PERM;
TRUNCATE TABLE MODULES;
TRUNCATE TABLE MODULE_CONTENT;
TRUNCATE TABLE QUIZ_QUESTIONS;
TRUNCATE TABLE QUIZ_ANSWERS;
TRUNCATE TABLE QUIZ_CORRECT;
TRUNCATE TABLE USER_PROGRESS;
TRUNCATE TABLE GRADEBOOK;

INSERT INTO MODULES (NAME, STATUS, BLURB) VALUES ("Phishes and Spam", "INACTIVE",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ullamcorper a arcu at congue. Maecenas nec commodo nisl, nec volutpat quam. Sed sit amet hendrerit libero. In eget ornare magna, eget malesuada diam. Fusce commodo sed neque et aliquam. Donec accumsan, dolor non ultricies molestie, urna nisl maximus justo, vitae facilisis tortor nisi a lorem. Pellentesque pulvinar magna ac augue dapibus ornare. Mauris gravida purus in felis gravida pretium. Fusce bibendum vestibulum nunc, ut euismod libero consectetur ut. Aliquam in lectus ut eros malesuada fringilla ac quis turpis. Nullam cursus felis vel orci elementum, tempor posuere lectus scelerisque. Proin malesuada rhoncus sapien vitae aliquet.");
INSERT INTO MODULES (NAME, STATUS, BLURB) VALUES ("Social Engineering", "ACTIVE",
    "Mauris at congue ante, non varius velit. Nunc ac rutrum neque, at molestie lorem. In semper turpis a neque posuere interdum. Donec id turpis id ex tempus semper. Nunc tempor purus quis nisi tincidunt gravida. Phasellus rhoncus gravida odio. Aenean congue vel ligula sit amet consequat. Duis efficitur leo vel nisl sollicitudin mollis. Nulla porta ipsum lectus, nec consequat nibh bibendum eu. Fusce mollis nisl eget dignissim rutrum. In ultrices iaculis nibh, sit amet fermentum risus. Quisque tempus, metus ac venenatis fermentum, mi lorem varius nisi, sit amet volutpat ante justo hendrerit odio. Sed blandit elit velit, sed euismod sapien vehicula at. Phasellus dignissim massa nisl, sed bibendum felis bibendum a.");
INSERT INTO MODULES (NAME, STATUS, BLURB) VALUES ("Choosing A Good Password", "ACTIVE",
    "Aliquam id odio laoreet, rutrum diam at, interdum quam. Donec quis laoreet metus. Suspendisse quis feugiat eros. Suspendisse potenti. Phasellus eget aliquet lectus. Nullam consequat, elit ac lacinia elementum, nulla turpis auctor nunc, sed lacinia leo enim id sem. Proin justo ex, dictum in urna ut, dignissim molestie ipsum.");

INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, CONTENT, EDITOR) VALUES (1, 1, '[{"TITLE":"s1", "CONTENT":"stuff"},{"TITLE":"s2", "CONTENT":"stuff"}]', 'uqcchua1');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, CONTENT, EDITOR) VALUES (1, 2, '[{"TITLE":"s1", "CONTENT":"stuff"},{"TITLE":"s2", "CONTENT":"stuff"}]', 'uqcchua1');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, CONTENT, EDITOR) VALUES (2, 1, '[{"TITLE":"s1", "CONTENT":"stuff"},{"TITLE":"s2", "CONTENT":"stuff"}]', 'uqcchua1');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, CONTENT, EDITOR) VALUES (2, 2, '[{"TITLE":"s1", "CONTENT":"stuff"},{"TITLE":"s2", "CONTENT":"stuff"}]', 'uqmcerva');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, CONTENT, EDITOR) VALUES (2, 3, '[{"TITLE":"s1", "CONTENT":"stuff"},{"TITLE":"s2", "CONTENT":"stuff"}]', 'uqcchua1');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, CONTENT, EDITOR) VALUES (3, 1, '[{"TITLE":"s1", "CONTENT":"stuff"},{"TITLE":"s2", "CONTENT":"stuff"}]', 'uqmcerva');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, CONTENT, EDITOR) VALUES (3, 2, '[{"TITLE":"s1", "CONTENT":"stuff"},{"TITLE":"s2", "CONTENT":"stuff"}]', 'uqmcerva');

INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (292, "Information Technology Services");
INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (123, "UQ Library");
INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (456, "Coffee Provisioners");

INSERT INTO ADMIN (USER_ID, NAME, UNIT_ID) VALUES ("uqcchua1", "Crystal", 292);
INSERT INTO ADMIN (USER_ID, NAME, UNIT_ID) VALUES ("uqmcerva", "Maria", 456);
INSERT INTO ADMIN (USER_ID, NAME, UNIT_ID) VALUES ("s4143179", "Daniel", 123);

INSERT INTO ADMIN_PERM (USER_ID, PERMISSION) VALUES ("uqcchua1", "read");
INSERT INTO ADMIN_PERM (USER_ID, PERMISSION) VALUES ("uqcchua1", "write");
INSERT INTO ADMIN_PERM (USER_ID, PERMISSION) VALUES ("uqmcerva", "write");

INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (2, "What are the two main types of social engineering?");
UPDATE MODULES SET NUM_QUIZ_QUESTIONS = NUM_QUIZ_QUESTIONS + 1 WHERE MODULE_ID = 2;
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (2, "Which of these options are not part of the cycle?");
UPDATE MODULES SET NUM_QUIZ_QUESTIONS = NUM_QUIZ_QUESTIONS + 1 WHERE MODULE_ID = 2;
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (2, "A co-worker found your bank details because you left your computer unlocked. What method of social engineering is this?");
UPDATE MODULES SET NUM_QUIZ_QUESTIONS = NUM_QUIZ_QUESTIONS + 1 WHERE MODULE_ID = 2;

INSERT INTO QUIZ_CORRECT (QUESTION_ID, ANSWER_ID) VALUES (1, 1);
INSERT INTO QUIZ_CORRECT (QUESTION_ID, ANSWER_ID) VALUES (2, 6);
INSERT INTO QUIZ_CORRECT (QUESTION_ID, ANSWER_ID) VALUES (3, 8);

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (1, "Technology-based and Human-based");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (1, "Waterholing and Baiting");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (1, "Viruses and Computer Theft");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (2, "Developing a Relationship");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (2, "Execution");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (2, "Evaluation");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (3, "Reverse Social Engineering");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (3, "Shoulder Surfing");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (3, "Dumpster Diving");

SET FOREIGN_KEY_CHECKS = 1;
