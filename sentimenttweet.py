import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt

class TwitterClient:

    def __init__(self):
#Enter your details
        consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error")
 
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|(http\S+)", " ", tweet).split())


    def get_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 500):

        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except :
            # print error (if any)
            print("Error")
            
def show_pie(pt,nt,neutral,query):

	labels = 'Positive', 'Negative', 'Neutral'
	sizes = [pt, nt, neutral]
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
	explode = (0.05, 0, 0)  # explode 1st slice

	plt.pie(sizes, explode=explode, labels=labels, colors=colors,
	        autopct='%1.1f%%', shadow=True, startangle=140)
	 
	plt.title("Search word: %s" %query)
	plt.axis('equal')
	plt.show()


def main():
	
	
	
	
    # creating object of TwitterClient Class
    api = TwitterClient()
	
	
	
    query = str(input("Enter the word to search: "))
	
    tweets = api.get_tweets(query = query, count = 500)
	
	
 
	
    # picking positive tweets from tweets
	
    
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
	 
    pt = 100*len(ptweets)/len(tweets)    
    print("Positive tweets percentage: ",pt," %")
	
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
	
	
    nt = 100*len(ntweets)/len(tweets)
    print("Negative tweets percentage: {} %".format(nt))
    # percentage of neutral tweets
    
    neutral = 100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
    print("Neutral tweets percentage: {} %".format(neutral))
 
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
        
    show_pie(pt,nt,neutral,query)
    
if __name__ == "__main__":
    main()
