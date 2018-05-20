#-*- coding:utf-8 -*-
from flask import Flask, request, make_response, redirect, url_for, session
from flask import render_template, render_template_string, flash, redirect, url_for, request
from cStringIO import StringIO
import random
from hashlib import md5

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = "hint:Secret_path_of_the_flag"

black_list = ['import', 'eval', 'exec', 'assert', '__dict__', '__globals__', '__init__', '__builtin__', '__builtins__', '__call__', 'reload', 'write','execfile', 'system', 'popen', 'decode', 'encode']

@app.route("/")
def index():
	auth = request.cookies.get("auth")
	if auth != None and auth == session['auth']:
		return redirect(url_for("draw"))		
	else:
		return render_template("index.html")

@app.route("/draw", methods=['POST', 'GET'])
def draw():
	number = random.randint(1,9)
	if request.method == 'POST':
		name = checkup(str(request.form['name']))
		if name:
			cookie = make_cookie(name, app.config['SECRET_KEY'])
			session['name'] = name
			session['auth'] = cookie
			response = make_response(render_template('user.html', name=name, number=number, lis=range(9)))
			response.set_cookie('auth', cookie)
			return response
		else:
			return render_template('sorry.html')
	if request.method == 'GET':
		auth = request.cookies.get("auth")
		if auth != None and auth == session['auth']:
			return render_template('user.html', name=session['name'], number=number, lis=range(9))
		else:
			return redirect(url_for("index"))

@app.route("/result", methods=['POST', 'GET'])
def res():
	if request.method == 'POST':
		number = str(request.form['number'])
		name = session['name']
		template = u'''
		{%% block body %%}
		<center>
		<h2>%s, 今天你的幸运数字是 %s.</h2>
		<h2>祝你今天交好运~</h2>
		<a href="/draw">我还想再抽</a>
		</center>
		{%% endblock %%}
		''' % (name, number)
		return render_template_string(template)
	elif request.method == 'GET':
		return redirect(url_for("index"))

@app.route("/clear")
def clear():
	response = make_response(render_template('index.html'))
	response.delete_cookie('auth')
	return response

@app.route("/test")
def test():
	return render_template('test.html')

@app.route("/Secret_path_of_the_flag")
def secret_path():
	return 'Oh you found me. Good job! Next, you need to read the flag in ./flag/flag.txt'

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'),500

def make_cookie(message, secret):
	return md5('%s%s' % (message, secret)).hexdigest()

def checkup(word):
	if word != '':
		for black in black_list:
			if black in word:
				return False
		return word
	else:
		return False

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
