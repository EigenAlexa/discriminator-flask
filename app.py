from flask import Flask
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handleRequest():
    text = request.form['text']
    return "Hi there! You said: {}".format(text)

if __name__ == '__main__':
    app.run(debug=True)
