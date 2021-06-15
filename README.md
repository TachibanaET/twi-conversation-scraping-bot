# twi-conversation-scraping

## 使い方

### Twitter Api キーの取得

### .envファイル
`.env_template`ファイルから`.env`ファイルを作成
```
cp .env_template .env
```

`.env`ファイルの中身を編集
Proxy設定は各自の環境に合わせてください。
API_TYPEは`standard`または`academic`を記入してください
```
BEARER_TOKEN=
API_TYPE=
```

### ビルド & 立ち上げ
```
docker-compose build
docker-compose up -d
```

### パラメータ
```
max_results : 一回のリクエストにつき、何件のTweetを取得するか
```

### 独自タスクを追加したい時
`index.py`にある`get_covid19_tweets()`関数を参考に作成