import threading
import tweepy
import time
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

#sets the status that is user input
def setStatus(status):
    #if the status is more than one character
    if len(status) > 1:
        api.update_status(status)
    else:
        #if its blank
        print("Did not send, Please enter a status.")

#unfollows people who unfollow the account
def unfollow(me, followersList, followingList):
    #goes through following
    for following in followingList:
        #if the account follows and they don't follow
        if following not in followersList:
            #unfollow
            api.destroy_friendship(following)
        
#retweets & follow if they tag the account
def retweetStatus(me, timeline, followersList):
    #goes through timeline
    for mention in timeline:
        #gets info
        user = mention.user.id
        status = mention.id
        #make sure they follow the account
        for follower in followersList:
            #if they are
            if user == follower and mention.retweeted == False:
                if mention.retweeted == False:
                    #retweet
                    api.retweet(status)
                    #if not liked
                    if mention.favorited == False:
                        #calls the like function
                        likeStatus(status)
#like function
def likeStatus(statusId):
    #likes the status
    api.create_favorite(statusId)

#msg those who follow the account
def directMsg(me, followersList, followingList):
    #goes through followers
    for follower in followersList:
        #if follower isn't being followed
        if follower not in followingList:
            #follow them
            api.create_friendship(follower)
            #Dm them
            dm = api.send_direct_message(follower, "If you would like to have your tweets retweeted please follow the twitter @SupportStream_" + 
            " and use @SupportStream_ in your tweets.")

#a background thread to run while main is running
def continuousRun():
    #the accounts id
    me = api.me().__dict__.get("id")
    #runs every 15 min
    retweetThread = threading.Timer(900.0, continuousRun)
    #stops when the main thread stops
    retweetThread.daemon = True
    #starts the thread
    retweetThread.start()
    #list of followers and following
    followers = []
    following = []
    timeline = []
    #mentions in timeline
    mentions = tweepy.Cursor(api.mentions_timeline).items()
    while True:
        try:
            #iterates through the mentions
            mention = next(mentions)
            #adds them to the timeline list
            timeline.append(mention)
        #if api rate limit exceeds
        except tweepy.TweepError:
            print("Rate Limit Reached")
            #wait 15 min
            time.sleep(60*15)
            #start again
            mention = next(mentions)
            timeline.append(mention)
        #at the end of mentions
        except StopIteration:
            break
    #item iteration 
    followersCheck = tweepy.Cursor(api.followers, id = me).items()
    #rate limiter check
    while True:
        try:
            #iterates through followerscheck
            follower = next(followersCheck)
            #adds it to the list
            followers.append(follower.id)
            #if limit is hit
        except tweepy.TweepError:
            print("Rate Limit Reached")
            #wait 15 min
            time.sleep(60*15)
            #repeat
            follower = next(followersCheck)
            followers.append(follower.id)
            #at the end of iteration
        except StopIteration:
            break

    #item iteration
    friendsCheck = tweepy.Cursor(api.friends, id = me).items()
    #rate limiter check
    while True:
        try:
            #iterates through friendscheck
            friends = next(friendsCheck)
            #adds it to the list
            following.append(friends.id)
            #if limit is hit
        except tweepy.TweepError:
            print("Rate Limit Reached")
            #wait 15 min
            time.sleep(60*15)
            #repeat
            friends = next(friendsCheck)
            following.append(friends.id)
            #at the end of iteration
        except StopIteration:
            break
     #creates a list of friends -- follow each other
    #calls retweet func
    retweetStatus(me, timeline, followers)
    #calls dm func
    directMsg(me, followers, following)
    #calls unfollow func
    unfollow(me, followers, following)
    #everytime it runs its just prints running
    print("running")

continuousRun()