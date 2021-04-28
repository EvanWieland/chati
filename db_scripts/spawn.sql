CREATE DATABASE CHATI_DB;
USE CHATI_DB;

-- ************************************** USER
CREATE TABLE IF NOT EXISTS USER
(
 UserID     int NOT NULL AUTO_INCREMENT ,
 UserName   varchar(64) NOT NULL ,
 Email      varchar(64) NOT NULL ,
 Password   varchar(64) NOT NULL ,
 DateJoined datetime NOT NULL ,

PRIMARY KEY (UserID)
);


-- ************************************** PROFILE
CREATE TABLE IF NOT EXISTS PROFILE
(
 ProfileID int NOT NULL AUTO_INCREMENT ,
 UserID    int NOT NULL ,
 FirstName varchar(64) NOT NULL ,
 LastName  varchar(64) NOT NULL ,
 Gender    char NULL ,
 About     text NOT NULL ,
 DateBorn  date NOT NULL ,

PRIMARY KEY (ProfileID),
KEY fkIdx_58 (UserID),
CONSTRAINT FK_57 FOREIGN KEY fkIdx_58 (UserID) REFERENCES USER (UserID)
);


-- ************************************** HASHTAG
CREATE TABLE IF NOT EXISTS HASHTAG
(
 HashtagID int NOT NULL AUTO_INCREMENT ,
 Hashtag   varchar(24) NOT NULL ,

PRIMARY KEY (HashtagID)
);


-- ************************************** POST
CREATE TABLE IF NOT EXISTS POST
(
 PostID     int NOT NULL AUTO_INCREMENT ,
 UserID     int NOT NULL ,
 HashtagID  int NULL ,
 Content    text NOT NULL ,
 DatePosted datetime NOT NULL ,

PRIMARY KEY (PostID),
KEY fkIdx_146 (HashtagID),
CONSTRAINT FK_145 FOREIGN KEY fkIdx_146 (HashtagID) REFERENCES HASHTAG (HashtagID),
KEY fkIdx_78 (UserID),
CONSTRAINT FK_77 FOREIGN KEY fkIdx_78 (UserID) REFERENCES USER (UserID)
);


-- ************************************** LIKE
CREATE TABLE IF NOT EXISTS `LIKE`
(
 LikeID    int NOT NULL AUTO_INCREMENT ,
 UserID    int NOT NULL ,
 PostID    int NOT NULL ,
 DateLiked datetime NOT NULL ,

PRIMARY KEY (LikeID),
KEY fkIdx_130 (PostID),
CONSTRAINT FK_129 FOREIGN KEY fkIdx_130 (PostID) REFERENCES POST (PostID),
KEY fkIdx_133 (UserID),
CONSTRAINT FK_132 FOREIGN KEY fkIdx_133 (UserID) REFERENCES USER (UserID)
);


-- ************************************** COMMENT
CREATE TABLE IF NOT EXISTS COMMENT
(
 CommentID     int NOT NULL AUTO_INCREMENT ,
 UserID        int NOT NULL ,
 PostID        int NOT NULL ,
 Comment       text NOT NULL ,
 DateCommented datetime NOT NULL ,

PRIMARY KEY (CommentID),
KEY fkIdx_86 (UserID),
CONSTRAINT FK_85 FOREIGN KEY fkIdx_86 (UserID) REFERENCES USER (UserID),
KEY fkIdx_97 (PostID),
CONSTRAINT FK_96 FOREIGN KEY fkIdx_97 (PostID) REFERENCES POST (PostID)
);


-- ************************************** FOLLOWING
CREATE TABLE IF NOT EXISTS FOLLOWING
(
 FollowingID    int NOT NULL AUTO_INCREMENT ,
 UserID         int NOT NULL ,
 FollowedUserID int NOT NULL ,
 DateFollowed   datetime NOT NULL ,

PRIMARY KEY (FollowingID),
KEY fkIdx_109 (UserID),
CONSTRAINT FK_108 FOREIGN KEY fkIdx_109 (UserID) REFERENCES USER (UserID),
KEY fkIdx_121 (FollowedUserID),
CONSTRAINT FK_120 FOREIGN KEY fkIdx_121 (FollowedUserID) REFERENCES USER (UserID)
);
