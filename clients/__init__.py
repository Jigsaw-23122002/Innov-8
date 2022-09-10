from flask import Flask
from flask_mde import Mde

app = Flask(__name__)
mde = Mde(app)
app.config['SECRET_KEY']='2f8a6f92623d8a218b15ecf6'

from clients import routes