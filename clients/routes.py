from flask import redirect, render_template, flash, request
from flask import Flask
from clients import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')
