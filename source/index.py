import datetime
import logging
import os
import time

import schedule

from file import FileClass
from network import NetworkClass
from utility import UtilityClass

logging.basicConfig(level=logging.INFO, format=' %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BEARER_TOKEN = os.environ['BEARER_TOKEN']
proxies = {
    "http": os.environ['http_proxy'],
    "https": os.environ['https_proxy']
}
api_type = os.environ['API_TYPE']

tweet_fields = [
    'id',
    'text',
    'created_at',
    'author_id',
    'conversation_id',
    'in_reply_to_user_id',
    'geo',
    'context_annotations',
    'referenced_tweets'
]

max_results = {
    'standard': 10,
    'academic': 20,
}


network = NetworkClass(api_type, BEARER_TOKEN, proxies)
utility = UtilityClass()

# example - covid-19


def get_covid19_tweets() -> None:
    logger.info('get covid19 tweets - start')
    save_path = '/workspace/default_save_dir/covid-19'
    file = FileClass(save_path)

    now_utc = datetime.datetime.utcnow()
    start_utc = now_utc - datetime.timedelta(hours=1)
    start_time = f'{start_utc.year}-{start_utc.month}-{start_utc.day}T{start_utc.hour}:00:00.000Z'
    end_time = f'{start_utc.year}-{start_utc.month}-{start_utc.day}T{start_utc.hour}:59:59.000Z'

    query = f'コロナ&start_time={start_time}&end_time={end_time}'
    single_tweets = network.get_tweets(
        query=query,
        tweet_fields=tweet_fields,
        max_results=max_results[api_type])

    single_tweets = utility.clean_new_line_char(tweets=single_tweets)

    conversation_ids = utility.get_conversation_ids(single_tweets)

    conversation_tweets = network.get_conversation_tweets(
        conversation_ids=conversation_ids,
        tweet_fields=tweet_fields,
        max_results=max_results[api_type])

    # result_text = json.dumps(
    #     conversation_tweets,
    #     indent=4,
    #     sort_keys=True,
    #     ensure_ascii=False)

    for idx, tweets in conversation_tweets.items():
        conversation_tweets[idx] = utility.clean_new_line_char(tweets=tweets)

    dir_name = f'{start_utc.year}-{start_utc.month}-{start_utc.day}T{start_utc.hour}'
    file.save_tweets(
        tweets_type='single',
        dir_name=dir_name,
        tweets=single_tweets)
    file.save_tweets(
        tweets_type='conversation',
        dir_name=dir_name,
        tweets=conversation_tweets)

    time.sleep(3)
    file.make_archive_and_clean_up(dir_name=dir_name)
    logger.info('get covid19 tweets - done')


if __name__ == '__main__':
    schedule.every(1).hours.do(get_covid19_tweets)

    while True:
        schedule.run_pending()
        time.sleep(1)
