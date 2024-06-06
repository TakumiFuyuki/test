from flask import Flask, render_template, request
from google.cloud import bigquery
from datetime import datetime

app = Flask(__name__)

# Google Cloud BigQueryのクライアントを初期化します
client = bigquery.Client()

# BigQueryのデータセット名とテーブル名を定義します
dataset_name = 'gifted-fragment-425209-s7.datasets'
button_table = 'button'
text_table = 'text'

@app.route('/')
def index():
    return render_template('submit.html')

@app.route('/submit', methods=['POST'])
def submit():
    # ボタンが押された時刻を取得します
    button_time = datetime.now()

    # フォームからボタンの種類を取得します、nameの部分を書き込む
    button_type = request.form['button_type']

    #フォームからテキストの内容を取得します
    text_input = request.form['text_input']

    # BigQueryにデータを挿入します
    insert_button_data_to_bigquery(button_time, button_type)
    insert_text_data_to_bigquery(button_time, text_input)

    # BigQueryから最新10件のテキストデータを取得します
    latest_text_data = get_latest_text_data()
    # return 'エラー確認'
    return latest_text_data

def insert_button_data_to_bigquery(button_time, button_type):
    # datetimeオブジェクトをISOフォーマットの文字列に変換
    button_time_iso = button_time.isoformat()
    # BigQueryに挿入する行のデータを準備
    rows_to_insert = [
        {
            "datetime": button_time_iso,
            "type": button_type
        }
    ]

    # BigQueryのテーブルにデータを挿入
    table_id = f"{dataset_name}.{button_table}"
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        raise Exception(f"BigQueryへのデータ挿入中にエラーが発生しました: {errors}")

def insert_text_data_to_bigquery(button_time, text_input):
    # datetimeオブジェクトをISOフォーマットの文字列に変換
    button_time_iso = button_time.isoformat()
    # BigQueryに挿入する行のデータを準備
    rows_to_insert = [
        {
            "datetime": button_time_iso,
            "text": text_input
        }
    ]

    # BigQueryのテーブルにデータを挿入
    table_id = f"{dataset_name}.{text_table}"
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        raise Exception(f"BigQueryへのデータ挿入中にエラーが発生しました: {errors}")

def get_latest_text_data():
    # BigQueryから最新のテキストデータを取得します
    query = f"""
        SELECT *
        FROM `{dataset_name}.{text_table}`
        ORDER BY datetime DESC
        LIMIT 1
    """
    query_job = client.query(query)
    results = query_job.result()

    # 結果を辞書のリストに変換します
    latest_data = [dict(row) for row in results]
    return latest_data

if __name__ == '__main__':
    app.run(port=8080)
