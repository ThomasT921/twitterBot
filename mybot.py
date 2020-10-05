import threading
import tweepy
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
me = api.me().__dict__.get("id")
followersList = api.followers_ids(me)
followingList = api.friends_ids(me)
timeline = api.mentions_timeline()


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
    for follower in followersList:
        friendships = api.show_friendship(source_id = me, target_id = follower)
        for friendship in friendships:
            if friendship.following == False:
                api.create_friendship(follower)
                api.send_direct_message(follower, "If you would like to have your tweets retweeted please follow the twitter @SupportStream_" + 
                " and use @SupportStream_ in your tweets.")


def continuousRun():
    me = api.me().__dict__.get("id")
    retweetThread = threading.Timer(1200.0, continuousRun)
    retweetThread.daemon = True
    retweetThread.start()
    retweetStatus(me, timeline, followersList)
    directMsg(me, followersList)
    unfollow(me, followersList, followingList)
    print("running")
