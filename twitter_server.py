import os
from flask import Flask, request, jsonify
from flask_cors import CORS

import tweepy

# Twitter API Config
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
bearer_token = os.environ['BEARER_TOKEN']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Tweetの検索上限数
tweet_search_limit = 10

# Flask Config
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False # 日本語化
CORS(app)

@app.route('/search', methods=['GET'])
def search():
  query = request.args.get('q')
  search_results = tweepy.Cursor(api.search, q=query).items(tweet_search_limit)
  resp_tweets = []
  for tweet in search_results:
    resp_tweets.append({
      "name": tweet.user.name,
      "screen_name": tweet.user.screen_name,
      "profile_image_url_https": tweet.user.profile_image_url_https,
      "text": tweet.text,
    })
    print("============")
    print("name:", tweet.user.name)
    print("screen_name:", tweet.user.screen_name)
    print("image_url:", tweet.user.profile_image_url_https)
    print("text:", tweet.text)
  return jsonify(resp_tweets)

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)