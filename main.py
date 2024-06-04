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

    # BigQueryにデータを挿入します
    insert_data_to_bigquery(button_time, button_type)
    return '提出が完了しました。'


def insert_data_to_bigquery(button_time, button_type):
    # データをBigQueryのテーブルに挿入するためのクエリを作成します
    query = f"""
        INSERT INTO '{dataset_name}.{table_name}' (datetime, type)
        VALUES ('{button_time}', '{button_type}')
    """

    # クエリを実行します
    client.query(query)

if __name__ == '__main__':
    app.run(port=8080)