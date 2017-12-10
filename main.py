import twitterToolz

_api = {
    "consumerKey" : "mhgITMt1lKmWFdDsNB4MBHa6L",
    "consumerSecret" : "q0iRrqy1riOjooLMk0S70uwoYCKYv7czgzDCxwirODGHu7d7cX",
    "accessToken" : "827624499977740290-khre9rbcYlBh8tK3AmfLImt3KOcNYrK",
    "accessTokenSecret" : "kVuoU9byF9F8tVCvHeqjWebsQkVfQAITis3zBRygEfa3j",
}

test = twitterToolz.mkm(_api)

# test.getTimeline()
# test.searchTwitter("#SundayMorning")
test.searchTwitter("#AMJoy")
# test.unfollowUsers()
# test.destroyAllTweets()
# test.destroyAllFavs()
