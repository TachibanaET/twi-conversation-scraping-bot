class UtilityClass():
    def __init__(self) -> None:
        pass

    def get_conversation_ids(self, tweets: list) -> list:
        conversation_ids = []
        for tweet in tweets:
            if(tweet['conversation_id'] not in conversation_ids) and (tweet['id'] != tweet['conversation_id']):
                conversation_ids.append(tweet['conversation_id'])

        return conversation_ids

    def clean_new_line_char(self, tweets: list) -> list:
        for idx, tweet in enumerate(tweets):
            tweets[idx]['text'] = tweet['text'].replace('\n', '')

        return tweets
