import tweepy

consumer_key = "0GCoGKT0GLdvVAsCsK45k1eIY"
consumer_secret = "yzA4xfUaMUOOfTYlBtbOwUgWyLWJu3kbNvhD9xwNcvheRUdXEv"
access_token = "1225820738-kLjqpN12UsNJCv0gsjquTXHDesLkLphvhYeIYJZ"
access_token_secret = "jZDJixuhJmPXsxSZPGoYEdeci0zCu2Cly9uiuHO3WRMAU"


def get_api_handler():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api
