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

INSERT INTO MODULES (NAME, STATUS, BLURB, NUM_QUESTIONS) VALUES ("Phishes and Spam", "INACTIVE",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ullamcorper a arcu at congue. Maecenas nec commodo nisl, nec volutpat quam. Sed sit amet hendrerit libero. In eget ornare magna, eget malesuada diam. Fusce commodo sed neque et aliquam. Donec accumsan, dolor non ultricies molestie, urna nisl maximus justo, vitae facilisis tortor nisi a lorem. Pellentesque pulvinar magna ac augue dapibus ornare. Mauris gravida purus in felis gravida pretium. Fusce bibendum vestibulum nunc, ut euismod libero consectetur ut. Aliquam in lectus ut eros malesuada fringilla ac quis turpis. Nullam cursus felis vel orci elementum, tempor posuere lectus scelerisque. Proin malesuada rhoncus sapien vitae aliquet.", 3
);
INSERT INTO MODULES (NAME, STATUS, BLURB, NUM_QUESTIONS) VALUES ("Social Engineering", "ACTIVE",
    "Mauris at congue ante, non varius velit. Nunc ac rutrum neque, at molestie lorem. In semper turpis a neque posuere interdum. Donec id turpis id ex tempus semper. Nunc tempor purus quis nisi tincidunt gravida. Phasellus rhoncus gravida odio. Aenean congue vel ligula sit amet consequat. Duis efficitur leo vel nisl sollicitudin mollis. Nulla porta ipsum lectus, nec consequat nibh bibendum eu. Fusce mollis nisl eget dignissim rutrum. In ultrices iaculis nibh, sit amet fermentum risus. Quisque tempus, metus ac venenatis fermentum, mi lorem varius nisi, sit amet volutpat ante justo hendrerit odio. Sed blandit elit velit, sed euismod sapien vehicula at. Phasellus dignissim massa nisl, sed bibendum felis bibendum a.", 2
);
INSERT INTO MODULES (NAME, STATUS, BLURB, NUM_QUESTIONS) VALUES ("Choosing A Good Password", "INACTIVE",
    "Aliquam id odio laoreet, rutrum diam at, interdum quam. Donec quis laoreet metus. Suspendisse quis feugiat eros. Suspendisse potenti. Phasellus eget aliquet lectus. Nullam consequat, elit ac lacinia elementum, nulla turpis auctor nunc, sed lacinia leo enim id sem. Proin justo ex, dictum in urna ut, dignissim molestie ipsum.", 4
);

INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, EDITOR) VALUES (1, 1, 'uqcchua1');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, EDITOR) VALUES (1, 2, 'uqcchua1');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, EDITOR) VALUES (2, 1, 'uqcchua1');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, EDITOR) VALUES (2, 2, 'uqmcerva');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, EDITOR) VALUES (2, 3, 'uqcchua1');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, EDITOR) VALUES (3, 1, 'uqmcerva');
DO SLEEP(30);
INSERT INTO MODULE_CONTENT (MODULE_ID, REVISION, EDITOR) VALUES (3, 2, 'uqmcerva');

INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (292, "Information Technology Services");
INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (123, "UQ Library");
INSERT INTO ORG_UNITS (UNIT_ID, UNIT_NAME) VALUES (456, "Coffee Provisioners");

INSERT INTO ADMIN (USER_ID, NAME, UNIT_ID) VALUES ("uqcchua1", "Crystal", 292);
INSERT INTO ADMIN (USER_ID, NAME, UNIT_ID) VALUES ("uqmcerva", "Maria", 456);

INSERT INTO ADMIN_PERM (USER_ID, PERMISSION) VALUES ("uqcchua1", "read");
INSERT INTO ADMIN_PERM (USER_ID, PERMISSION) VALUES ("uqcchua1", "write");

INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (1, "Best kind of cake?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (1, "Where is bear?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (1, "Where's Wally?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (2, "Cat?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (2, "Dog?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (3, "Breakfast?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (3, "Lunch?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (3, "Dinner?");
INSERT INTO QUIZ_QUESTIONS (MODULE_ID, QUESTION) VALUES (3, "Dessert?");

INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (1, 3);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (2, 5);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (3, 8);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (4, 10);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (5, 15);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (6, 16);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (7, 20);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (8, 24);
INSERT INTO CORRECT_ANSWERS (QUESTION_ID, ANSWER_ID) VALUES (9, 22);

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (1, "Tiramisu");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (1, "Blackforest");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (1, "Any cake");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (2, "Twelve-Acre Wood");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (2, "Hundred-Acre Wood");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (2, "Forty-Five-Acre Wood");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (3, "Somewhere");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (3, "Nowhere");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (3, "Everywhere");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (4, "Nova");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (4, "Pretzel");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (4, "Poppy");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (5, "Corgi");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (5, "German Shepherd");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (5, "Finnish Lapphund");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (6, "Waffles");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (6, "Bagel");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (6, "Cereal");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (7, "Noodles");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (7, "Sushi");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (7, "Pies");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (9, "Ice Cream");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (8, "Spaghetti");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (8, "Mac and Cheese");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (8, "Lasagne");

INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (9, "Chocolate Fondue");
INSERT INTO QUIZ_ANSWERS (QUESTION_ID, ANSWER) VALUES (9, "Frozen Yogurt");

INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 1, 1);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 2, 5);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 3, 9);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 4, 10);
INSERT INTO GRADEBOOK (USER_ID, ORG_UNIT, QUESTION_ID, ANSWER_ID) VALUES ("s1234567", "CATS", 5, 13);

SET FOREIGN_KEY_CHECKS = 1;
