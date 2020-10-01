from flask import render_template, redirect, url_for, jsonify, request
from flask import current_app as app
from application.athoc.sendAtHock import AtHock
from . import analyzer
import configparser
from .twitterbot import replyTweet
import uuid
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze/', methods=['post', 'get'])
def analyze():
    if request.method == 'POST':
        location = request.form.get('location')
        account = request.form.get('account')
        number_of_tweets = int(request.form.get('number_of_tweets'))
        print(location)
        print(account)
        negative_tweets = analyzer.find_negative_tweets_to_account(account, number_of_tweets)
        print(negative_tweets)

        categorized_negative_tweets = analyzer.categorize_tweets(negative_tweets)

        return render_template("results.html", negative_tweets=negative_tweets, categories=categorized_negative_tweets)

@app.route('/createticket/<string:username>/<string:tweet_id>')
def createticket(username, tweet_id):
    uuid4 = uuid.uuid1()
    message = "We have created a ticket {uuid} to track and resolve this issue".format(uuid=str(uuid4))
    replyTweet(username,tweet_id,message)
    return render_template('index.html')


@app.route('/sendalert/<string:tweet_id>')
def sendalert(tweet_id):
    config = configparser.ConfigParser()
    config.read_file(open(r'atHoc.cfg'))
    client_id = config.get('AtHocToken', 'client_id')
    client_secret = config.get('AtHocToken', 'client_secret')
    username = config.get('AtHocToken', 'username')
    password = config.get('AtHocToken', 'password')
    common_name = config.get('AtHocPublish', 'common_name')
    base_url = config.get('AtHocToken', 'base_url')
    org = config.get('AtHocToken', 'org')

    atHock = AtHock(client_id, client_secret, username, password, org, base_url)
    token_result = atHock.get_bearer_token()

    if token_result.status_code != 200:
        print("Failed to get access token. HTTP {}. Caused by {}.".format(token_result.status_code,
                                                                          token_result.json()['error']))
        print("Double Check your atHoc.cfg for correct values!")
        return
    else:
        print("[Success] got access token!")

    access_token = token_result.json()['access_token']

    html = "https://twitter.com/x/status/{tweet_id}".format(tweet_id=tweet_id)

    publish_result = atHock.publish_alert(access_token, common_name, "Alert: Tweet deemed actionable",
                                          "This tweet was deemed by operator to be an issue Tweet: {tweet_html} Follow link for live heatmap of issues. https://encodehackathonteambb2020.azurewebsites.net/".format(tweet_html=html), "https://311heatmapencode2020.azurewebsites.net/")

    if publish_result.status_code != 200:
        print("Failed to publish alert! HTTP {}. Caused by {}.".format(publish_result.status_code,
                                                                       publish_result.json()['error']))
        return
    else:
        print("[Success] posted Alert. Audit ID: {}".format(publish_result.json()['Auid']))
    return render_template('index.html')
