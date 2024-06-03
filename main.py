# main.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('submit.html')

# @app.route('/submit', methods=['post'])
# def submit():
#     return '提出が完了しました。'

if __name__ == '__main__':
    app.run(port=8080)