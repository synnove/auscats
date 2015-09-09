SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE ORG_UNITS;
TRUNCATE TABLE ADMIN;
TRUNCATE TABLE ADMIN_PERM;
TRUNCATE TABLE MODULES;
TRUNCATE TABLE MODULE_CONTENT;
TRUNCATE TABLE QUIZ_QUESTIONS;
TRUNCATE TABLE QUIZ_ANSWERS;
TRUNCATE TABLE CORRECT_ANSWERS;
TRUNCATE TABLE USER_PROGRESS;
TRUNCATE TABLE GRADEBOOK;

INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (292, "Information Technology Services");
INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (123, "UQ Library");
INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (456, "Coffee Provisioners");

INSERT INTO ADMIN (USER_ID, NAME, UNIT_ID) VALUES ("uqcchua1", "Crystal", 292);
INSERT INTO ADMIN (USER_ID, NAME, UNIT_ID) VALUES ("uqmcerva", "Maria", 456);

INSERT INTO ADMIN_PERM (USER_ID, PERMISSION) VALUES ("uqcchua1", "read");
INSERT INTO ADMIN_PERM (USER_ID, PERMISSION) VALUES ("uqcchua1", "write");

INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (1, "Hello?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (1, "Where is bear?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (1, "Cat?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (2, "Thing?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (2, "What?");

INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (1, 2);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (2, 4);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (3, 9);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (4, 11);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (5, 13);

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (1, "A");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (1, "B");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (1, "C");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (2, "D");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (2, "E");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (2, "F");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (3, "G");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (3, "H");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (3, "I");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (4, "J");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (4, "K");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (4, "L");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (5, "M");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (5, "N");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (5, "O");

INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s4367459", "EAIT", 1, 2);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s4367459", "EAIT", 2, 4);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s4367459", "EAIT", 3, 7);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s4367459", "EAIT", 4, 11);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s4367459", "EAIT", 5, 13);

INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 1, 1);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 2, 5);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 3, 9);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 4, 10);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 5, 13);

INSERT INTO MODULES (NAME, BLURB) VALUES ("Phishes and Spam",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ullamcorper a arcu at congue. Maecenas nec commodo nisl, nec volutpat quam. Sed sit amet hendrerit libero. In eget ornare magna, eget malesuada diam. Fusce commodo sed neque et aliquam. Donec accumsan, dolor non ultricies molestie, urna nisl maximus justo, vitae facilisis tortor nisi a lorem. Pellentesque pulvinar magna ac augue dapibus ornare. Mauris gravida purus in felis gravida pretium. Fusce bibendum vestibulum nunc, ut euismod libero consectetur ut. Aliquam in lectus ut eros malesuada fringilla ac quis turpis. Nullam cursus felis vel orci elementum, tempor posuere lectus scelerisque. Proin malesuada rhoncus sapien vitae aliquet."
);
INSERT INTO MODULES (NAME, BLURB) VALUES ("Social Engineering", 
    "Mauris at congue ante, non varius velit. Nunc ac rutrum neque, at molestie lorem. In semper turpis a neque posuere interdum. Donec id turpis id ex tempus semper. Nunc tempor purus quis nisi tincidunt gravida. Phasellus rhoncus gravida odio. Aenean congue vel ligula sit amet consequat. Duis efficitur leo vel nisl sollicitudin mollis. Nulla porta ipsum lectus, nec consequat nibh bibendum eu. Fusce mollis nisl eget dignissim rutrum. In ultrices iaculis nibh, sit amet fermentum risus. Quisque tempus, metus ac venenatis fermentum, mi lorem varius nisi, sit amet volutpat ante justo hendrerit odio. Sed blandit elit velit, sed euismod sapien vehicula at. Phasellus dignissim massa nisl, sed bibendum felis bibendum a."
);
INSERT INTO MODULES (NAME, BLURB) VALUES ("Choosing A Good Password",
    "Aliquam id odio laoreet, rutrum diam at, interdum quam. Donec quis laoreet metus. Suspendisse quis feugiat eros. Suspendisse potenti. Phasellus eget aliquet lectus. Nullam consequat, elit ac lacinia elementum, nulla turpis auctor nunc, sed lacinia leo enim id sem. Proin justo ex, dictum in urna ut, dignissim molestie ipsum."
);
SET FOREIGN_KEY_CHECKS = 1;
