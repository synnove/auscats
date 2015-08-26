SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE ADMIN;
TRUNCATE TABLE COURSES;
TRUNCATE TABLE COURSE_CONTENT;
TRUNCATE TABLE QUESTIONS;
TRUNCATE TABLE ANSWERS;
TRUNCATE TABLE QUIZ_QUESTIONS;
TRUNCATE TABLE QUIZ_ANSWERS;
TRUNCATE TABLE QUIZ_CORRECT;
TRUNCATE TABLE USER_PROGRESS;
TRUNCATE TABLE GRADEBOOK;

INSERT INTO ADMIN (USERID) VALUES ("uqcchua1");

INSERT INTO COURSES (NAME, BLURB) VALUES ("Phishes and Spam",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ullamcorper a arcu at congue. Maecenas nec commodo nisl, nec volutpat quam. Sed sit amet hendrerit libero. In eget ornare magna, eget malesuada diam. Fusce commodo sed neque et aliquam. Donec accumsan, dolor non ultricies molestie, urna nisl maximus justo, vitae facilisis tortor nisi a lorem. Pellentesque pulvinar magna ac augue dapibus ornare. Mauris gravida purus in felis gravida pretium. Fusce bibendum vestibulum nunc, ut euismod libero consectetur ut. Aliquam in lectus ut eros malesuada fringilla ac quis turpis. Nullam cursus felis vel orci elementum, tempor posuere lectus scelerisque. Proin malesuada rhoncus sapien vitae aliquet."
);
INSERT INTO COURSES (NAME, BLURB) VALUES ("Social Engineering", 
    "Mauris at congue ante, non varius velit. Nunc ac rutrum neque, at molestie lorem. In semper turpis a neque posuere interdum. Donec id turpis id ex tempus semper. Nunc tempor purus quis nisi tincidunt gravida. Phasellus rhoncus gravida odio. Aenean congue vel ligula sit amet consequat. Duis efficitur leo vel nisl sollicitudin mollis. Nulla porta ipsum lectus, nec consequat nibh bibendum eu. Fusce mollis nisl eget dignissim rutrum. In ultrices iaculis nibh, sit amet fermentum risus. Quisque tempus, metus ac venenatis fermentum, mi lorem varius nisi, sit amet volutpat ante justo hendrerit odio. Sed blandit elit velit, sed euismod sapien vehicula at. Phasellus dignissim massa nisl, sed bibendum felis bibendum a."
);
INSERT INTO COURSES (NAME, BLURB) VALUES ("Choosing A Good Password",
    "Aliquam id odio laoreet, rutrum diam at, interdum quam. Donec quis laoreet metus. Suspendisse quis feugiat eros. Suspendisse potenti. Phasellus eget aliquet lectus. Nullam consequat, elit ac lacinia elementum, nulla turpis auctor nunc, sed lacinia leo enim id sem. Proin justo ex, dictum in urna ut, dignissim molestie ipsum."
);
SET FOREIGN_KEY_CHECKS = 1;
