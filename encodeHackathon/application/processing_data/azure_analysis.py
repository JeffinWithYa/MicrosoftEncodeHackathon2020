from application.processing_data.twitter import TwitterAPIv2
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from .twitter import TwitterAPIv2

categories={
    'Noise Complaints': {
        'loud',
        'party',
        'noisy',
        'noise',
        'hear',
        'music',
    },
    'Animal Services' : {
        'dog',
        'cat',
        'bird',
        'rabbit',
        'dead',
    },
    'Un-Sanitary conditions': {
        'dirty',
        'trash',
        'mess',
        'gross',
        'litter',
    },
    'Water Infrastructure' : {

    },
    'Broken Roads' : {

    }
}

def authenticate_client():
    key = <key>
    endpoint = 'https://textanalysishackathon.cognitiveservices.azure.com/'
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

def filterNegativeTweets(tweets):
    client = authenticate_client()
    negative_tweets = []
    documents = []
    for tweet in tweets:
        documents.append(tweet['text'])
    response = client.analyze_sentiment(documents=documents)
    twitterAPI = TwitterAPIv2()
    result = [doc for doc in response if not doc.is_error]
    #Iterate over the tweets and match them to the response values
    for tweet in tweets:
        for document in result:
            #Tweet matches the document
            if document.sentences[0].text in tweet['text']:
                #if document is negative, save both the tweet, document, and get the keyphrases
                if document.confidence_scores.negative >= 0.5:
                    negative_tweets.append({
                        'tweet': tweet,
                        'sentiment': document,
                        'key_phrases': client.extract_key_phrases(documents=[tweet['text']])[0],
                        'tweet_location_data' : twitterAPI.get_tweet_with_id_location(tweet['id'])
                    })
                break

    return negative_tweets
