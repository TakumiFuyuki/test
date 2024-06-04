from flask import Flask, render_template, request
from google.cloud import bigquery
from datetime import datetime

app = Flask(__name__)

# Google Cloud BigQueryのクライアントを初期化します
client = bigquery.Client()

# BigQueryのデータセット名とテーブル名を定義します
dataset_name = 'gifted-fragment-425209-s7.datasets'
table_name = 'button'

@app.route('/')
def index():
    return render_template('submit.html')

@app.route('/submit', methods=['POST'])
def submit():
    # ボタンが押された時刻を取得します
    button_time = datetime.now()

    # フォームからボタンの種類を取得します
    button_type = request.form['button_type']

    # BigQueryにデータを挿入します
    insert_data_to_bigquery(button_time, button_type)
    return '提出が完了しました。'

def insert_data_to_bigquery(button_time, button_type):
    # BigQueryに挿入する行のデータを準備
    rows_to_insert = [
        {
            "datetime": button_time,
            "type": button_type
        }
    ]

    # BigQueryのテーブルにデータを挿入
    table_id = f"{dataset_name}.{table_name}"
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        raise Exception(f"BigQueryへのデータ挿入中にエラーが発生しました: {errors}")

if __name__ == '__main__':
    app.run(port=8080)
