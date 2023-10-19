# Fargate + Dashによるダッシュボードアプリケーションの実装

## 概要
以下の構成のダッシュボードアプリケーションを構築する。

<img src="./images/dash_app.drawio.png">

1. EventBridgeをトリガーに毎日指定時刻になったらOpen Weather APIから天気予報情報(json形式)を取得しS3に格納。

2. Athenaを用いてS3のjsonファイルからスキーマ, ビューを作成し、Glueデータカタログに登録する。

3. 1とは別のEventBridgeルールをトリガーに毎日指定時刻になったらダッシュボードに表示するための最新情報を取得しS3に格納。

4. ECRで管理しているコンテナイメージを基にFargat上でDashアプリケーションを稼働。参照元データは3で取得した情報の格納先S3バケット。



## リポジトリの構成
**Docker image 構築用資材**  
* `Dockerfile`
  * コンテナイメージ作成用ファイル
* `mnt/requirements.txt`
  * コンテナにインストールするpythonパッケージリスト
* `mnt/execute.sh`  
  * コンテナ起動時に実行するスクリプト

**Lambda関数のコード**
* `lambda/get_info.py`
  * Open Wheahter API から天気予報情報を取得するためのコード
* `lambda/update_data.py`
  * Dash が参照するデータを更新するためのコード

**ダッシュボード構築用資材**
* `mnt/run.py`
  * Dash 起動用コード
* `mnt/pages/`  
  * 各ページのレイアウトなどを定義しているファイル
* `mnt/assets/style.css`
  * ナビゲーションバーのスタイルを変更するためのファイル
* `mnt/module/boto3.py` 
  * S3からcsvファイルを取得するためのモジュール
