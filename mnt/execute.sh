# クレデンシャル情報の取得s
AWS_CONTAINER_CREDENTIAL=`curl -s http://169.254.170.2$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI`
export AWS_ACCESS_KEY_ID=`echo "$AWS_CONTAINER_CREDENTIAL" | jq .AccessKeyId -r`
export AWS_SECRET_ACCESS_KEY=`echo "$AWS_CONTAINER_CREDENTIAL" | jq .SecretAccessKey -r`
export AWS_SESSION_TOKEN=`echo "$AWS_CONTAINER_CREDENTIAL" | jq .Token -r`

# run.pyを実行。引数にクレデンシャル情報を渡す。
python3 run.py $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_SESSION_TOKEN
