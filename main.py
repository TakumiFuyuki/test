# main.py

from flask import Flask, render_template, request
from google.cloud import bigquery #install
from datetime import datetime

app = Flask(__name__)

# Google Cloud BigQueryのクライアントを初期化します
client = bigquery.Client()

# BigQueryのデータセット名とテーブル名を定義します
dataset_name = 'datasets'
table_name = 'button'

@app.route('/')
def index():
    return render_template('submit.html')

@app.route('/submit', methods=['post']) #htmlでpathを設定する必要がある
def submit():
    # ボタンが押された時刻を取得します
    button_time = datetime.now()

    # フォームからボタンの種類を取得します
    button_type = request.form['button_type']

    # # BigQueryにデータを挿入します
    # insert_data_to_bigquery(button_time, button_type)
    return '提出が完了しました。'


# def insert_data_to_bigquery(button_time, button_type):
#     # ボタン時刻をUNIXタイムスタンプに変換
#     button_time_timestamp = button_time.timestamp()

#     # クエリの準備
#     query = """
#         INSERT INTO `{dataset_name}.{table_name}` (datetime, type)
#         VALUES (@button_time, @button_type)
#     """.format(dataset_name=dataset_name, table_name=table_name)

#     # クエリパラメータの設定
#     job_config = bigquery.QueryJobConfig(
#         query_parameters=[
#             bigquery.ScalarQueryParameter("button_time", "TIMESTAMP", button_time_timestamp),
#             bigquery.ScalarQueryParameter("button_type", "STRING", button_type),
#         ]
#     )

#     # クエリを実行
#     client.query(query, job_config=job_config)

if __name__ == '__main__':
    app.run(port=8080)