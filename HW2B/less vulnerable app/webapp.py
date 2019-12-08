#!/usr/bin/env python3
from os import popen
from flask import Flask, render_template, request

app = Flask(__name__)

# app_path = os.path.dirname(os.path.abspath(__file__))
word = None

@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('home.html', title='Home')

@app.route('/redword')
def redword():
    return render_template('redword.html', title='Red Word')

@app.route('/getip')
def getip():
    return render_template('getip.html', title='Get IP')

@app.route('/returnred', methods=['POST'])
def return_red():
    if request.method == 'POST':
        word = request.form['word']
    return render_template('returnred.html', title='Is it red?', word=word)

@app.route('/getipresult', methods=['POST'])
def getipresult():
    if request.method == 'POST':
        domain_name = request.form['domain']
    for i in domain_name.split('.'):
        for supposed_letter in i:
            if supposed_letter.isalnum():
                continue
            return render_template('getipresult.html', title='IP Result', domain="Sorry. Not valid.")
    result = popen('nslookup {}'.format(domain_name)).read()
    result = result.split(' ')[-1]
    return render_template('getipresult.html', title='IP Result', domain=result)

if __name__ == '__main__':
    app.run(debug=True)
