from .processing_data.twitter import TwitterAPIv1

def replyTweet(username, tweet_id, message):
    reply = '@{username} {message}'.format(username=username, message=message)
    twitterAPI = TwitterAPIv1()
    twitterAPI.reply_to_tweet(tweet_id, reply)