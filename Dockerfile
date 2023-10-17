# aws cliを利用するためAmazonLinuxイメージをベースにする
FROM public.ecr.aws/amazonlinux/amazonlinux:latest

# linuxの環境設定
# 更新可能なパッケージ一覧をアップデートして、パッケージを更新する。
RUN yum update -y \
    # pipとjqのインストール
    && yum install -y python-pip jq

# 作業するディレクトリの変更
WORKDIR /home
# 資材のコピー
# COPY {コピーしたいファイルのパス} {コンテナ上のコピーしたい場所のパス}
COPY ./mnt/ ${PWD}

# pythonのパッケージをインストール
RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 8050

# コマンドの実行
CMD ["sh", "./execute.sh"]














