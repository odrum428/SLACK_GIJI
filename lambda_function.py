import json
import threading
from post_message_to_slack import post_message_to_slack, post_thread_message

# 並列処理して重複メッセージをはじく
def lambda_handler(event, context):
    thread_1 = threading.Thread(target=return_200)
    thread_2 = threading.Thread(target=main_func(event, context))
    return 0

def return_200():
    return 0

def main_func(event, context):
    print(event)
    # Slackからのリクエストがリトライ処理であるかを確認
    if 'X-Slack-Retry-Num' in event['params']['header']:
        print("this is redirect request!.")
        return 0

    post_text = event['body']['event']['text']
    channel = event['body']['event']['channel']
    message_ts = event['body']['event']['ts']

    if 'start_mtg' in post_text:
        message = "MTGを始めるよ！参加する人はjoin、興味がある人はwatchをスレッドに書き込んでね！"
        post_message_to_slack(message, channel)
        return 0

    if 'end_mtg' in post_text:
        message = "MTGを終了したよ！このスレッドの内容は以下のリンクに書き込んでおいたよ！\n https://www.google.com/"
        res = post_thread_message(message, channel, message_ts)
        return 0

    message = "そんなコマンドはないよ！以下でヘルプを確認してね"
    post_message_to_slack(message, channel)
    return 0
