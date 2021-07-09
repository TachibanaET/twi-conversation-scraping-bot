import json
import os
import time
from logging import getLogger

import requests

logger = getLogger('twi-conversation-scraping')


class NetworkClass():

    def __init__(
            self,
            api_type: str,
            BEARER_TOKEN: str,
            proxies: dict) -> None:
        self.api_type = api_type
        self.BEARER_TOKEN = BEARER_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.BEARER_TOKEN}"
        }
        self.proxies = proxies

    def connect_to_endpoint(self, url: str) -> dict:
        time.sleep(1)
        response = requests.request(
            "GET", url, headers=self.headers, proxies=self.proxies)
        if response.status_code != 200:
            logger.exception(f'Exception: {response.text}')

        return response.json()

    def create_endpoint_url(self,
                            query: str,
                            tweet_fields: list,
                            max_results: int,
                            next_token: str = '',
                            with_next_token: bool = False,
                            ) -> str:
        formatted_tweet_fields = ''
        if any(tweet_fields):
            formatted_tweet_fields = ",".join(tweet_fields)

        endpoint = 'recent' if self.api_type == 'standard' else 'all'
        formatted_query = ''
        if with_next_token:
            formatted_query = f'query={query}&tweet.fields={formatted_tweet_fields}&max_results={max_results}&next_token={next_token}'

        else:
            formatted_query = f'query={query}&tweet.fields={formatted_tweet_fields}&max_results={max_results}'
        endpoint_url = f'https://api.twitter.com/2/tweets/search/{endpoint}?{formatted_query}'
        return endpoint_url

    def get_tweets(
            self,
            query: str,
            tweet_fields: list,
            max_results: int) -> list:

        tweets = []
        with_next_token = False
        next_token = ''
        # 参照するページ数 : 10
        for i in range(10):

            endpoint_url = self.create_endpoint_url(
                query=query,
                tweet_fields=tweet_fields,
                max_results=max_results,
                next_token=next_token,
                with_next_token=with_next_token,
            )

            json_response = self.connect_to_endpoint(endpoint_url)
            tmp_tweets = json_response['data']
            tweets += tmp_tweets

            if json_response['meta']['next_token']:
                break

            else:
                with_next_token = True
                next_token = json_response['meta']['next_token']

        return tweets

    def _get_root_tweet(
            self,
            conversation_id: str,
            tweet_fields: list) -> dict:

        formatted_tweet_fields = ''
        if any(tweet_fields):
            formatted_tweet_fields = ",".join(tweet_fields)

        endpoint_url = f'https://api.twitter.com/2/tweets/{conversation_id}?tweet.fields={formatted_tweet_fields}'
        json_response = self.connect_to_endpoint(endpoint_url)
        try:
            return json_response['data']
        except Exception as e:
            logger.exception(e)
            return ''

    def get_conversation_tweets(
            self,
            conversation_ids: list,
            tweet_fields: list,
            max_results: int) -> dict:
        conversation_tweets = {}
        for conversation_id in conversation_ids:
            logger.info(f'get conversation : {conversation_id}')
            try:
                # root tweet
                root_tweet = self._get_root_tweet(
                    conversation_id=conversation_id,
                    tweet_fields=tweet_fields)
                if root_tweet == '':
                    continue
                conversation_tweets[conversation_id] = []
                conversation_tweets[conversation_id].append(root_tweet)

            except Exception as e:
                logger.exception(e)
                continue

            # reply tweets
            query = f'conversation_id:{conversation_id}'
            endpoint_url = self.create_endpoint_url(
                query=query,
                tweet_fields=tweet_fields,
                max_results=max_results
            )
            json_response = self.connect_to_endpoint(endpoint_url)
            reply_tweets = json_response['data']

            for rep in reversed(reply_tweets):
                tmp_rep = rep
                for i in rep['referenced_tweets']:
                    if i['type'] == 'replied_to':
                        tmp_rep['reply_to_id'] = i['id']
                conversation_tweets[conversation_id].append(tmp_rep)

        return conversation_tweets
