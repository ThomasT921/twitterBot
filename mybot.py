import threading
import tweepy
import time
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
me = api.me().__dict__.get("id")
data = api.rate_limit_status()
print (data['resources']['followers'])

friend = api.show_friendship(source_id = me, target_id = "1312457044784566276")
print (friend)
#sets the status that is default or user inputs
def setStatus(status):
    if len(status) > 1:
        api.update_status(status)
    else:
        print("Did not send, Please enter a status.")

def unfollow(me, followersList, followingList):
    for following in followingList:
        if following not in followersList:
            api.destroy_friendship(following)
        

def retweetStatus(me, timeline, followersList):
    for mention in timeline:
        user = mention.user.id
        status = mention.id
        for follower in followersList:
            if user == follower and mention.retweeted == False:
                api.retweet(status)
                if mention.favorited == False:
                    likeStatus(status)

def likeStatus(statusId):
    api.create_favorite(statusId)

#msg those who follow the account
def directMsg(me, followersList):
    friendships = []
    for follower in followersList:
        while True:
            try:
                friendship = api.show_friendship(source_id = me, target_id = follower)
                friendships.append(friendship)
            except tweepy.TweepError:
                time.sleep(60*15)
                friendship = api.show_friendship(source_id = me, target_id = follower)
                friendships.append(friendship)
            except StopIteration:
                break
    print(friendships)
    for friendship in friendships:
        if friendship.following == False:
            api.create_friendship(follower)
            dm = api.send_direct_message(follower, "If you would like to have your tweets retweeted please follow the twitter @SupportStream_" + 
            " and use @SupportStream_ in your tweets.")


def continuousRun():
    me = api.me().__dict__.get("id")
    retweetThread = threading.Timer(950.0, continuousRun)
    retweetThread.daemon = True
    retweetThread.start()
    followers = []
    following = []
    timeline = api.mentions_timeline(me)

    followersCheck = tweepy.Cursor(api.followers, id = me).items()

    while True:
        try:
            follower = next(followersCheck)
            followers.append(follower.id)
        except tweepy.TweepError:
            time.sleep(60*15)
            follower = next(followersCheck)
            followers.append(follower.id)
        except StopIteration:
            break
    print(followers)

    friendsCheck = tweepy.Cursor(api.friends, id = me).items()
    while True:
        try:
            friends = next(friendsCheck)
            following.append(friends.id)
        except tweepy.TweepError:
            time.sleep(60*15)
            friends = next(friendsCheck)
            following.append(friends.id)
        except StopIteration:
            break
    print(following)
    retweetStatus(me, timeline, followers)
    directMsg(me, followers)
    unfollow(me, followers, following)
    print("running")
