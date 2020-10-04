import threading
import tweepy
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

#timeline = api.mentions_timeline()
#for mention in timeline:
    #print(str(mention.in_reply_to_user_id) + "--" + str(mention.id) + "--" + str(mention.text) + "--" + str(mention.user.id))
    #         this is me ^                              status id^               status text^               who sent the status^
    #print(mention.__dict__.values())

#sets the status that is default or user inputs
def setStatus(status):
    #needs to have an if statement
    # if defualt
    # api.update --- defualt status 
    # if user input
    # add validation to make sure they enter something
    # api.update -textinput
    # add validation making sure they wnat to tweet it with the tweet in the message.
    print("Worked") #text is the text of the tweet
    pass

def unfollow(me):
    followersList = api.followers_ids(me)
    followingList = api.friends_ids(me)
    for following in followingList:
        if following not in followersList:
            api.destroy_friendship(following)
        

def retweetStatus(me):
    timeline = api.mentions_timeline()
    followersList = api.followers_ids(me)
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
def directMsg(me):
    followersList = api.followers_ids(me) 
    for follower in followersList:
        friendships = api.show_friendship(source_id = me, target_id = follower)
        print(friendships)
        for friendship in friendships:
            if friendship.following == False:
                api.create_friendship(follower)
                api.send_direct_message(follower, "If you would like to have your tweets retweeted please follow the twitter @SupportStream_" + 
                " and use @SupportStream_ in your tweets.")


def continuousRun():
    me = api.me().__dict__.get("id")
    retweetThread = threading.Timer(900.0, continuousRun)
    retweetThread.daemon = True
    retweetThread.start()
    retweetStatus(me)
    directMsg(me)
    unfollow(me)
    print("running")
