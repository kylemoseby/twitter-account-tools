# import json
import csv
from threading import Timer

import tweepy


class mkm():
    apiCalls = 0

    def __init__(self, api):

        print "Initialising Twitter Account Tools"
        print "Authorizing usage with Twitter API."

        # Tweept Authorization Stuff
        auth = tweepy.OAuthHandler(api.get("consumerKey"), api.get("consumerSecret"))
        auth.set_access_token(api.get("accessToken"), api.get("accessTokenSecret"))
        auth = tweepy.OAuthHandler(api.get("consumerKey"), api.get("consumerSecret"))
        auth.set_access_token(api.get("accessToken"), api.get("accessTokenSecret"))

        # Twitter class
        self._tweepy_ = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        print "Authorization successfull with Twitter."

    def getTimeline(self):
        self.my_tweets = self._tweepy_.user_timeline()

    def retweetCleanup(self):

        if self.my_tweets:

            for tweet in self.my_tweets:
                if tweet.retweeted:
                    self.apiThrottle(call=self._tweepy_.destroy_status,data=tweet.id)
                    print "   Retweet "+ tweet.id_str + " has been destroyed"

            self.getTimeline()
            self.retweetCleanup()

        else:
            print "There are no tweet currently associated with this account"

    def tweetsWriteToCSV(self):
        # print "Writing tweets for " + "username" + " to CSV"

        tweet_csv = open("username.csv", "wb")
        writer = csv.writer(tweet_csv, quotechar='"', quoting=csv.QUOTE_ALL)

        ifile = open('test.csv', "rb")
        reader = csv.reader(ifile)

        # Add tweets to file
        for tweet in self.my_tweets:
            print tweet
            writer.writerow()

    def destroyAllTweets(self):
        pass

        if self.my_tweets.__len__() is not None:
            for tweet in self.my_tweets:
                print "Destroying status: " + tweet.id._str
                self._tweepy_.destroy_status(tweet.id)

    def searchTwitter(self, term):

        # print "Getting search for " + term

        results = self._tweepy_.search(q=term)

        print results.__len__()

        self.processTweets(results)

    def processTweets(self, twresults):

        for tweet in twresults:

            print tweet.text

            try:
                self.apiThrottle(call=self._tweepy_.create_friendship, data=tweet.user.id)

                # print "Following " + tweet.user.screen_name
            except:
                print "Could not follow the user, probably already following"

            # try:
            #     self._tweepy_.retweet(tweet.id)
            #     print "  Retweeting tweet"
            #
            # except:
            #     print "Couldn't retweet, probably already retweeted."
            #
            # try:
            #     self._tweepy_.create_favorite(tweet.id)
            #     print "  Favorite tweet"
            #
            # except:
            #     print "Couldn't favorite tweet, probably already favorited"

        # try:
        # print "Replying"
        # self._tweepy_.update_status("@" + tweet.user.screen_name + " Totes bruh!! #SeguimeYTeSigo #FollowBack #motivation  Right on my man!! #" + term, in_reply_to_status_id=tweet.id)
        # except:
        #     print "Counldn't add your status bruh"

    def apiThrottle(self, call, data):

        api_status = self._tweepy_.rate_limit_status()

        remaining_usage = api_status.get("resources").get("application").get("/application/rate_limit_status").get("remaining")

        self.apiCalls += 1

        print "   Total calls " + self.apiCalls.__str__()
        print "    Remaining calls " + remaining_usage.__str__()

        if remaining_usage > 5:
            return call(data)
        else:

            print "Waiting before next call..."

            return Timer(100, call(data))

    def destroyAllFavs(self):

        def getFavs():
            favList = self._tweepy_.favorites()
            favs_cnt = favList.__len__()

            print "Twitter returned " + favs_cnt.__str__() + " favorites"

            return favList

        def unfavTweet(_id_):
            self.apiThrottle(call=self._tweepy_.destroy_favorite, data=_id_)
            print "    Destroyed: " + _id_.__str__()

        def processFavs(_favs_):
            if _favs_:
                for fav in _favs_:
                    unfavTweet(fav.id)

                processFavs(getFavs())
            else:
                print "There are no more favorites associated with this account."

        favs = getFavs()

        processFavs(favs)

    def unfollowUsers(self):

        def getIDs():
            return self._tweepy_.friends_ids()

        def unfollow(_id_):
            print "   Unfollowing " + _id_.__str__()
            self._tweepy_.destroy_friendship(user_id=_id_)

        following = getIDs()

        def unfollowFollowing(queue):
            if queue:
                # Unfollow users
                for id in queue:
                    self.apiThrottle(call=unfollow, data=id)

                # Check for more followers
                unfollowFollowing(getIDs())
            else:
                print "User is not following anyone!!!"

        unfollowFollowing(following)
