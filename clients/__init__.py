from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']='2f8a6f92623d8a218b15ecf6'

from clients import routes