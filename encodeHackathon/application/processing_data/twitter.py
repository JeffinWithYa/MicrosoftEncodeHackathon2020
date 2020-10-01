import requests
import json
import urllib.parse
import oauth2 as oauth
import tweepy
class TwitterAPIv1:

    def __init__(self):
        consumer_key = <your_consumer_key>
        consumer_secret = <your_consumer_secret>
        access_token = <access_token>
        access_token_secret = <access_token_secret>

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)
        return




    def reply_to_tweet(self, tweet_id, reply):
        self.api.update_status(reply,tweet_id)
        return
        # endpoint = 'https://api.twitter.com/1.1/statuses/update.json?status={reply}&in_reply_to_status_id={tweet_id}'.format(reply=reply, tweet_id=tweet_id)
        # response, data = self.client.request(endpoint, "POST")
        # print(response)
        # print(data)
        # return


class TwitterAPIv2:
    def __init__(self):
        self.api_key = <api_key>
        self.api_secret_key = <api_secret>
        self.bearer_token = <token>

    def get_tweets_about(self, entity):
        endpoint = 'https://api.twitter.com/2/tweets/search/recent?query=entity:\"{}\"'.format(entity)
        headers = {
            'Authorization': 'Bearer ' + self.bearer_token,
        }
        r = requests.get(endpoint, headers=headers)
        return json.loads(r.content)

    def get_next_tweets_to(self, account, next_token):
        endpoint = 'https://api.twitter.com/2/tweets/search/recent?query=to:{account}&expansions=author_id&next_token={next_token}&user.fields=username'.format(account=account,next_token=next_token)
        headers = {
            'Authorization': 'Bearer ' + self.bearer_token,
        }
        r = requests.get(endpoint, headers=headers)
        return json.loads(r.content)

    def get_users_with_ids(self, ids):
        endpoint = 'https://api.twitter.com/2/users?ids={}'.format(','.join(ids))
        headers = {
            'Authorization': 'Bearer ' + self.bearer_token,
        }
        r = requests.get(endpoint, headers=headers)
        return json.loads(r.content)

    def get_tweets_to(self, account, pages):
        endpoint = 'https://api.twitter.com/2/tweets/search/recent?query=to:{}&expansions=author_id&user.fields=username'.format(account)
        headers = {
            'Authorization': 'Bearer ' + self.bearer_token,
        }
        r = requests.get(endpoint, headers=headers)

        json_response = json.loads(r.content)
        all_tweets = json_response['data'].copy()
        if pages is 1:
            return all_tweets
        else:
            for i in range(pages):
                next_token = json_response['meta'].get('next_token', None)
                if next_token:
                    json_response = self.get_next_tweets_to(account, json_response['meta']['next_token'])
                    all_tweets.extend(json_response['data'].copy())
                    continue
            return all_tweets
    def get_tweet_with_id_location(self, id):
        endpoint = 'https://api.twitter.com/2/tweets?ids={tweet_id}&expansions=geo.place_id&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type'.format(tweet_id=id)
        headers = {
            'Authorization': 'Bearer ' + self.bearer_token,
        }
        r = requests.get(endpoint, headers=headers)
        return json.loads(r.content)
