from flask import Flask
from supabase import create_client, Client
from localStoragePy import localStoragePy

app = Flask(__name__)
app.config['SECRET_KEY']='2f8a6f92623d8a218b15ecf6'
supabase: Client = create_client("https://yuhrnfjyvvbluvhlpbhm.supabase.co",
                                 "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1aHJuZmp5dnZibHV2aGxwYmhtIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjIyOTQzOTYsImV4cCI6MTk3Nzg3MDM5Nn0.ueJAWAmBuCAE4wvCvSihgiWcS73S8hsbT0CiiICRhdo")
localStorage = localStoragePy('supabase.authentication', 'json')

from clients import routes