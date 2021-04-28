import os
import random
import string
import datetime
import re

import pandas as pd
import lorem

data_dir = '../data/reports'
max_txt_len = 280  # 120
hashtag_count = 30

# Yeah, it's ugly, but it works. I don't really care if I can't understand it a year from now or
# it takes an extra 10sec to crunch.

def mung():
    idx = 0

    master_df = None

    users = []
    profiles = []
    posts = []
    comments = []
    hashtags = {'wow': 1, 'awesome': 2}

    post_idx = 1
    comment_idx = 1

    for entry in os.scandir(data_dir):
        # For testing
        # if idx == 3:
        #     break

        if entry.path.endswith('.csv') and entry.is_file():
            idx += 1
            print('Sanitizing [%s]: %s' % (idx, entry.path))

            df = pd.read_csv(entry.path)
            comment_df = df

            # Reverse order
            df.reindex(index=df.index[::-1])

            # Remove undesired data
            del df['Tweet URL']
            del df['Verified or Non-Verified']
            del df['Profile URL']
            del df['Protected or Not Protected']
            del df['Retweets received']
            del df['Likes received']
            del df['User Id']
            # Good data el
            del df['Client']

            df.rename(columns={'Tweet Id': 'PostID', 'Tweet Content': 'Content', 'Tweet Posted Time': 'DatePosted'},
                      inplace=True)

            # Find comments
            comment_df = df.loc[df['Tweet Type'] != 'Tweet']

            df.drop(df.loc[df['Tweet Type'] != 'Tweet'].index, inplace=True)
            df.reset_index(drop=True, inplace=True)

            # COMMENT
            for i, row in comment_df.iterrows():
                comment = []
                comment.append(comment_idx)
                comment.append(idx)
                comment.append(None)
                comment.append(
                    re.sub(r'\w*#\w*', '', truncate_string(comment_df.loc[i, 'Content'].encode('unicode-escape').decode('ASCII').replace('"', ''), max_txt_len)))
                comment.append(None)
                comment_idx += 1

                comments.append(comment)

            # POST & HASHTAG
            for i, row in df.iterrows():
                post = []
                post.append(post_idx)
                post.append(idx)
                post.append(truncate_string(df.loc[i, 'Content'].encode('unicode-escape').decode('ASCII').replace('"', ''), max_txt_len))
                post.append(str(df.loc[i, 'DatePosted']))
                post_idx += 1
                hts = [s for s in str(df.loc[i, 'Content']).encode('unicode-escape').decode('ASCII').lower().split() if s.startswith('#')]
                if hts:
                    ht = ''.join(e for e in hts[0] if e.isalpha())
                    # Only one hashtag per post
                    post[2] = '#' + ht + ' ' + re.sub(r'\w*#\w*', '', post[2])

                    if str(ht) in hashtags and not (hashtags[str(ht)] is None):
                        post.append(str(hashtags[str(ht)]))
                    elif str(ht) != '':
                        hashtags[str(ht).replace('#', '')] = len(hashtags) + 1
                        post.append(str(hashtags[str(ht)]))
                posts.append(post)

            # PROFILE
            profile = []
            profile.append(idx)
            profile.append(idx)
            name = df['Name'].iat[0].replace('"', '').split(' ', 1)
            profile.append(name[0])
            profile.append(name[len(name) - 1])
            profile.append(rand_gender())
            profile.append(truncate_string(lorem.paragraph(), 120))
            profile.append(rand_date(datetime.datetime(1940, 1, 1), datetime.datetime(2008, 1, 1)))
            profiles.append(profile)

            # USER
            user = []
            user.append(idx)
            user.append(df['Username'].iat[0])
            user.append(rand_email(name[0].replace(' ', '')))
            user.append(rand_str(10, 16))
            user.append(df['DatePosted'].iloc[-1])
            users.append(user)

            if idx == 1:
                master_df = df
            else:
                master_df = pd.concat([master_df, df])

    # FOLLOWING
    print('Generating FOLLOWING')
    following = []
    f_idx = 1
    f_rand_idx = len(users) * (len(users) - len(users) / 2)
    while f_rand_idx > 0:
        u1 = random.choice(users)
        u2 = random.choice(users)
        # Don't allow a user to follow themselves
        if u1[0] != u2[0]:
            dates = [datetime.datetime.strptime(u1[4], '%Y-%m-%d %H:%M:%S'),
                     datetime.datetime.strptime(u2[4], '%Y-%m-%d %H:%M:%S')]
            follow = [f_idx, u1[0], u2[0], min(dates)]

            unique = True
            for f in following:
                if (f[1] == follow[1]) and (f[2] == follow[2]):
                    # Won't add to list if already exists
                    unique = False
                    continue

            if unique:
                following.append(follow)
                f_idx += 1
                f_rand_idx -= 1

    # HASHTAG
    print('Generating HASHTAG')
    ht_data = []
    for ht in hashtags:
        ht_data.append([hashtags[ht], ht])

    # COMMENT
    print('Generating COMMENT')
    c_idx = 0
    for c in comments:
        post = None
        while post is None:
            p = random.choice(posts)
            # Make sure the post and comment are from different users
            if p[1] != c[1]:
                post = p

        # Set PostID
        c[2] = post[0]
        # Set date
        c[4] = post[3]

        comments[c_idx] = c
        c_idx += 1

    # LIKE
    print('Generating LIKE')
    likes = []
    l_idx = 1
    l_rand_idx = len(posts) * .5
    while l_rand_idx > 0:
        post = random.choice(posts)
        user = random.choice(users)
        # Don't allow a user to like their own post
        if user[0] != post[1]:
            like = [l_idx, post[1], post[0], post[3]]

            unique = True
            for l in likes:
                if (l[1] == like[1]) and (l[2] == like[2]):
                    # Won't add to list if already exists
                    unique = False
                    continue

            if unique:
                likes.append(like)
                l_idx += 1
                l_rand_idx = l_rand_idx - 5

    user_df = pd.DataFrame(users, columns=['UserID', 'Username', 'Email', 'Password', 'DateJoined'])
    profile_df = pd.DataFrame(profiles,
                              columns=['ProfileID', 'UserID', 'FirstName', 'LastName', 'Gender', 'About', 'DateBorn'])
    post_df = pd.DataFrame(posts, columns=['PostID', 'UserID', 'Content', 'DatePosted', 'HashtagID'])
    comment_df = pd.DataFrame(comments, columns=['CommentID', 'UserID', 'PostID', 'Comment', 'DateCommented'])
    hashtag_df = pd.DataFrame(ht_data, columns=['HashtagID', 'Hashtag'])
    like_df = pd.DataFrame(likes, columns=['LikeID', 'UserID', 'PostID', 'DateLiked'])
    following_df = pd.DataFrame(following, columns=['FollowingID', 'UserID', 'FollowedUserID', 'DateFollowed'])

    print("Exporting CSV files")
    user_df.to_csv('./../data/sanitized/user.csv', index=None, header=True)
    profile_df.to_csv('./../data/sanitized/profile.csv', index=None, header=True)
    post_df.to_csv('./../data/sanitized/post.csv', index=None, header=True)
    comment_df.to_csv('./../data/sanitized/comment.csv', index=None, header=True)
    hashtag_df.to_csv('./../data/sanitized/hashtag.csv', index=None, header=True)
    like_df.to_csv('./../data/sanitized/like.csv', index=None, header=True)
    following_df.to_csv('./../data/sanitized/following.csv', index=None, header=True)

    # like_df.to_html('./../data_explore.html')

    print("Process complete")


def rand_email(s):
    return str.lower('%s@%s.com' % (s, rand_str(5, 9)))


def rand_gender():
    return random.choice(['F', 'M', 'O', None])


def rand_str(minlen, maxlen):
    return ''.join(random.choice(string.ascii_letters) for i in range(random.randint(minlen, maxlen)))


def rand_date(begin: datetime.datetime, end: datetime.datetime):
    epoch = datetime.datetime(1970, 1, 1)
    begin_seconds = int((begin - epoch).total_seconds())
    end_seconds = int((end - epoch).total_seconds())
    dt_seconds = random.randint(begin_seconds, end_seconds)

    return datetime.datetime.fromtimestamp(dt_seconds)


def truncate_string(value, max_length=255, suffix='...'):
    string_value = str(value)
    string_truncated = string_value[:min(len(string_value), (max_length - len(suffix)))]
    suffix = (suffix if len(string_value) > max_length else '')
    return string_truncated + suffix
