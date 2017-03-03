from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handleRequest():
    text = request.form['text']
    return "Hi there! You said: {}".format(text)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
