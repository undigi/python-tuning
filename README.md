# python-tuning

Pythonのチューニングポイントまとめ  

## FastAPI

基本的にFastAPIに作り直すと思う。。

## gunicorn

FastAPIはASGIミドルウェアのuvicornを使って動かす。  
プロセスはuvicornを利用し、プロセス管理はgunicornを利用する。  
起動コマンドは以下の通り。(main.pyで`app=Flask()`、もしくは`app=FastAPI()`となっていたとする)

```sh
gunicorn -k uvicorn.workers.UvicornWorker -c /path/to/gunicorn_conf.py main:app
```

### configuration

- accesslog
  - logファイルのパスを指定する
  - 最終的にoffにする
- errorlog
  - logファイルのパスを指定する
  - 最終的にoffにする
- sendfile
  - nginxのsendfileと同じ？(ファイルの中身をネットワークに転送するシステムコール)
  - デフォルト`False`
- deamon
  - daemon起動させる（systemdで起動させる時とか）
- bind
  - バインドするIPとport
- backlog
  - サービスを受けるのを待つことができるクライアントの数。
  - デフォルト2048
- workers
  - 起動する子プロセス数（ワーカー数）。デフォルト1
  - `2~4×${NUM_CORES}`くらいが望ましいが、チューニングが必要
- threads
  - リクエストを処理するためのワーカースレッド数。デフォルト1
  - `2~4×${NUM_CORES}`くらいが望ましいが、チューニングが必要
- worker_connections
  - クライアントが最大つなげるコネクション数。デフォルト1000
- max_requests
  - メモリリークしないように、N回リクエストを受け付けると自動再起動するようにできる。デフォルト0
  - 0の場合は設定がoffになる
- max_requests_jitter
  - max_requestsから`randint(0, max_requests_jitter)`分上乗せする。デフォルト0
  - workerプロセスごと違う値にできるので同時再起動が発生する確率を下げることができる
  - 0の場合は設定がoffになる
- timeout
  - タイムアウト値。デフォルト30秒
- graceful_timeout
  - 再起動時、gracefulに再起動できる
  - この値分待ってrequestがまだきている場合、強制的に再起動する。デフォルト30秒
- keepalive
  - デフォルト2秒
  - クライアントと直接つなぐ場合は1-5秒くらいに設定しておくといい
  - nginxなどの背後にある場合はnginxのkeepaliveよりも大きな値にする必要がある。(504エラーを返してしまうかも。。？)

## sqlalchemy

今のところ思いつくのはN + 1問題くらい。。([参考](https://aish.dev/misc/orm_n1problem.html))

```python
# N+1版
session = Session()
for table2 in session.query(Table2).all():
    table2.table1.text
```

```python
# selectinloadを使用
session = Session()
for t2 in session.query(Table2).options(selectinload(Table2.table1)).all():
    t2.table1.text
```
