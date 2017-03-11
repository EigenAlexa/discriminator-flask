from flask import Flask, request
from pymongo import MongoClient
import requests

app = Flask(__name__)
c = MongoClient('172.17.0.3',27017)

@app.route("/", methods=["POST"])
def handleRequest():
    text = request.form['text']
    user = request.form['user']
    sessionId = request.form['sessionId']
    print(user)
    response = discriminate(text)
    c.skilldata.msgs.insert({'request':text, 'response': response, 'session':sessionId, 'user': user})
    return response

def discriminate(text):
    try:
        res = requests.post('https://3ss5b0g2q4.execute-api.us-east-1.amazonaws.com/production',{'text':text})
        return str(res.content)
    except requests.exceptions.RequestException:
        return "Could you repeat that, please?"
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
    
