from flask import Flask, request
from pymongo import MongoClient
import requests
import re
import grequests

app = Flask(__name__)
c = MongoClient('172.17.0.3',27017)

from swearWords import words as swears
from swearWords import phrases

@app.route("/", methods=["POST"])
def handleRequest():
    text = request.form['text']
    user = request.form['user']
    sessionId = request.form['sessionId']
    print(user)
    if containsSwear(text):
        response = "I am not comfortable talking about that. Can we talk about something else?"
    elif asksForAdvice(text):
        response = "I don't think that I have the requisite knowledge to answer such a question."
    elif letsChatAbout(text):
        topic = letsChatAbout(text)
        response = "Okay, what specifically about " + topic + " do you want to talk about?"
    elif letsChat(text):
        response = "Okay, what do you want to talk about?"
    else:
        response = discriminate(text)
    c.skilldata.msgs.insert({'request':text, 'response': response, 'session':sessionId, 'user': user})
    return response

def discriminate(text):
    try:
        reqs = [ 
          grequests.post('https://3ss5b0g2q4.execute-api.us-east-1.amazonaws.com/production', data={'text':text}),
          grequests.get('http://107.22.159.20', params={'q': text} )
        ]
        aiml_res, goog_res = grequests.map(reqs)
        if goog_res and goog_res.text != 'Hello' and goog_res.text != 'Query not found':
            return goog_res.text
        elif aiml_res:
            return aiml_res.text
        else:
            return "Could you repeat that, please?"
    except requests.exceptions.RequestException:
        return "Could you repeat that, please?"

def containsSwear(text):
    words = re.split(";|,|\:|\.|\?|\-|\!| |", text)
    hasSwear = any(word.lower().startswith(swear) and word.lower().endswith(swear) for word in words for swear in swears)
    hasBadPhrase = any(phrase in text for phrase in phrases)
    return hasSwear or hasBadPhrase

def asksForAdvice(text):
    return "should I" in text or "advice" in text

def letsChat(text):
    return "let's chat" in text

def letsChatAbout(text):
    return "let's chat about" in text and text.split("let's chat about")[-1]
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
    
