'''retrieve tweets from twitter by username and add to database, return tweet
vector'''

import requests
import ast
import spacy

from .models import DB, User, Tweet

nlp = spacy.load('my_nlp_model')


def vectorize_tweet(tweet_text):
    '''return vector of tweet'''
    return nlp(tweet_text).vector


def get_user_and_tweets(username):
    '''get user and tweets from twitter'''

    HEROKU_URL = 'https://lambda-ds-twit-assist.herokuapp.com/user/'

    user = ast.literal_eval(requests.get(HEROKU_URL + username).text)

    try:
        if User.query.get(user['twitter_handle']['id']):
            db_user = User.query.get(user['twitter_handle']['id'])
        else:
            db_user = User(id=user['twitter_handle']['id'],
                           name=user['twitter_handle']['username'])
            DB.session.add(db_user)

        tweets_added = 0

        for tweet in user['tweets']:
            if Tweet.query.get(tweet['id']):
                break
            else:
                tweet_text = tweet['full_text']
                db_tweet = Tweet(
                    id=tweet['id'], text=tweet_text, vect=nlp(tweet_text).vector)
                db_user.tweets.append(db_tweet)
                DB.session.add(db_tweet)
                tweets_added += 1

    except Exception as e:
        raise e

    DB.session.commit()

    return tweets_added
