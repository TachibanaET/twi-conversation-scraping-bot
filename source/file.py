import json
import os
import shutil


class FileClass():
    def __init__(self, save_path) -> None:
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def save_tweets(
            self,
            tweets_type: str,
            dir_name: str,
            tweets: list) -> None:

        file_path = os.path.join(self.save_path, dir_name)
        os.makedirs(file_path, exist_ok=True)

        if tweets_type == 'single':
            with open(f'{file_path}/single_tweets.txt', 'w+') as f:
                for tweet in tweets:
                    f.write(json.dumps(tweet))
                    f.write('\n')

        elif tweets_type == 'conversation':
            for idx, tmp_tweets in tweets.items():
                with open(f'{file_path}/{idx}.txt', 'w+') as f:
                    for tweet in tmp_tweets:
                        f.write(json.dumps(tweet))
                        f.write('\n')

    def make_archive_and_clean_up(self, dir_name: str) -> None:
        file_path = os.path.join(self.save_path, dir_name)
        shutil.make_archive(file_path, 'tar', root_dir=file_path)
        shutil.rmtree(file_path)
