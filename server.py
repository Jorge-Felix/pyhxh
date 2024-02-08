from flask import Flask,render_template,redirect,url_for

app = Flask(__name__)


@app.route("/")
def index():
    return "Index"

if __name__ == '__main__':
    app.run(host = '127.0.0.1',port = 8888, debug = True)