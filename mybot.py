

import tweepy

consumer_key = "QuNadPar8VBpuYw3XJlmYQZkC"
consumer_secret = "BdfkGlw0pcYTfOI2p5KM7k6KxSXlcvlnejVRmGEa58FBc4PAvi"
access_token = "949582798700142592-mb1LNMnL4WZh4vOCxaAeC1abwBbHEBs"
access_token_secret = "JSeFit2now612KsQGGdRTbXt9Cn19WwFlmOpykiax63mN"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


