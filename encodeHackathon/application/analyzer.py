from .processing_data.azure_analysis import *

def categorize_tweets(negative_tweets):
    categories = {
        'Noise-Complaints' : ['loud', 'party', 'noisy', 'noise', 'hear', 'music', 'yell'],
        'Un-Sanitary-Conditions' : ['dirty', 'trash', 'gross', 'litter', 'waste', 'garbage', 'bin'],
        'Parking' : ['park', 'parking'],
        'Infrastructure' : ['pylons', 'sidewalk', 'intersection', 'lane', 'water', 'road', 'pothole'],
        'Covid': ['science', 'sick', 'testing', 'tested', 'virus', 'mask', 'pandemic'],
        'Other': []
    }
    categorized_neg_tweets = {}

    for category in categories:
        categorized_neg_tweets[category] = []

    for tweet in negative_tweets:
        found_category = False
        for key_word in tweet["key_phrases"]["key_phrases"]:
            for category in categories:
                for category_key_word in categories[category]:
                    if category_key_word in key_word.lower():
                        categorized_neg_tweets[category].append(tweet)
                        found_category = True
        if not found_category:
            categorized_neg_tweets['Other'].append(tweet)

    return categorized_neg_tweets





def find_negative_tweets_to_account(twitter_account, number_of_tweets):
    twitterAPI = TwitterAPIv2()
    tweets_to_account = twitterAPI.get_tweets_to(twitter_account, number_of_tweets//10)
    if len(tweets_to_account) > 10:
        negative_tweets = []
        #filter negative tweets goes through AZURE sentiment analysis which only allows 10 documents at a time
        #as a result, we have to rate limit on this end, only allow ten tweets to filter at a time.
        split_lists = [tweets_to_account[i:i+10] for i in range(0, len(tweets_to_account), 10)]
        for split_list in split_lists:
            print(split_list)
            negative_tweets.extend(filterNegativeTweets(split_list))
        match_negative_tweets_to_users(negative_tweets)
        return negative_tweets
    else:
        negative_tweets = filterNegativeTweets(tweets_to_account)
        match_negative_tweets_to_users(negative_tweets)
        return negative_tweets

#Given a set of tweets with "author ids", find their usernames and associate them with the user
#You need @usernames to be able to reply to tweets!
def match_negative_tweets_to_users(negative_tweets):
    user_ids = []
    for negative_tweet in negative_tweets:
        user_ids.append(negative_tweet["tweet"]["author_id"])

    twitterAPI = TwitterAPIv2()
    users = twitterAPI.get_users_with_ids(user_ids)

    for user in users["data"]:
        for negative_tweet in negative_tweets:
            if user["id"] == negative_tweet["tweet"]["author_id"]:
                negative_tweet["user"] = user
    return



