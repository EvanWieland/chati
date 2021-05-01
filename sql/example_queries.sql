-- Get all posts a certain user liked on a certain day.
SELECT *
FROM POST
WHERE PostID IN (SELECT DISTINCT PostID
FROM LIKES
WHERE UserID = 1 AND DateLiked LIKE '2019-09-14%')


-- Get the hashtag text on every one of a particular user's posts with a hashtag.
SELECT POST.UserID, HASHTAG.Hashtag
FROM HASHTAG
JOIN POST ON HASHTAG.HashtagID = POST.HashtagID AND UserId = 1;


-- Get the first user to join the platform.
SELECT UserID, Username, DateJoined
FROM USER
ORDER BY DateJoined ASC LIMIT 1;


-- Get the number of likes each user has given.
SELECT UserID, COUNT(LikeID) AS LikesGiven
FROM LIKES
GROUP BY UserID;


-- Get the users following a particular user.
SELECT UserID, Username
FROM USER
WHERE USER.UserID IN (SELECT FOLLOWING.UserID
FROM USER
JOIN FOLLOWING
ON USER.UserID = FollowedUserID
WHERE USER.UserID = 1);