from flask import Flask, render_template, url_for, session, request, redirect
import os

app = Flask(__name__)

@app.route('/')
def index():
    txt = '<a href="/quize/10/">ssylka</a>'
    txt2 = '<a href="/quize/30/">ssylka2</a>'
    return txt + txt2

# /quize/2/
@app.route('/quize/<int:id>/')
def quize(id):

    return id * ' Hello'

app.run()