from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
import json
from linkedin import LinkedInBot
import os
import openai

openai.api_key = os.getenv('OPENAI_SECRET')

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/linkedin', methods=['GET'])
def linkedin():
    auth = request.headers.get('Authorization')
    if auth is None:
        return json.dumps({'message': 'No authorization header'}), 401
    username, password = auth.split(':')

    bot = LinkedInBot()
    ret = bot.authenticate(username, password)
    if not ret:
        return json.dumps({'message': 'Wrong credentials'}), 401
    bot.fetch_conversations()
    packet = json.dumps({
        'username': username,
        'conversations': bot.conversations,
        'message': 'You are logged in!'
    })
    return packet, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)