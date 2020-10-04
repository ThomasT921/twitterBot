import tkinter as tk
import tweepy
import threading
from mybot import api

window = tk.Tk()
label = tk.Label(window, text="hello")

timeline = api.mentions_timeline()
for mention in timeline:
    print(str(mention.in_reply_to_user_id) + "--" + str(mention.id) + "--" + str(mention.text) + "--" + str(mention.user.id))
    #         this is me ^                              status id^               status text^               who sent the status^
    #print(mention.__dict__.values())
    print(mention.retweeted)
#for mention in timeline:
        #print(str(mention.in_reply_to_user_id) + "--" + str(mention.id) + "--" + str(mention.text))

#sets the status that is default or user inputs
def setStatus(text):
    #needs to have an if statement
    # if defualt
    # api.update --- defualt status 
    # if user input
    # add validation to make sure they enter something
    # api.update -textinput
    # add validation making sure they wnat to tweet it with the tweet in the message.
    api.update_status(text) #text is the text of the tweet
    pass

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


def retweeterRun():
    me = api.me().__dict__.get("id")
    retweetThread = threading.Timer(10.0, retweeterRun)
    retweetThread.daemon = True
    retweetThread.start()
    retweetStatus(me)
    directMsg(me)
    print("running")
    
class Gui:
    def __init__(self, master):
        self.__master = master
        self.__setSize()
        self.__close_button()
        self.__create_label("Tweet:")

    def __setSize(self):
        self.__master.minsize(1000,500)

    def __close_button(self):
        self.close_button = tk.Button(window, text="Close Button", command = self.__close)
        self.close_button.pack()
    
    def __send_button(self):
        self.send_button = tk.Button(window, text="Send") #command = send #function for sending a tweet
        self.send_button.pack()
    
    def __create_label(self, text):
        self.label = tk.Label(window, text=text)
        self.label.pack()

    def __close(self):
        self.__master.destroy()    

def main():
    me = api.me().__dict__.get("id")
    Gui(window)
    directMsg()
    #retweeterRun()
    #window.mainloop() 
    
main()