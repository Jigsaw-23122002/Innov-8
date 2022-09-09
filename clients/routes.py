import os
from flask import redirect, render_template,flash,request
from flask import Flask
from clients import app
from flask_sqlalchemy import SQLAlchemy
from supabase import create_client, Client
# from flask_graphql import GraphQLView
from python_graphql_client import GraphqlClient
# import requests





# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://innov-8.hasura.app/v1/graphql")
headers = { "x-hasura-admin-secret": "SLZkKBZbyB5qrPgJGM6e4ytxrEgDymSoZ756aSDkf8ky6cDYGRPFrc7D3alyV3fp" }
# Create the query string and variables required for the request.
query = """
query MyQuery {
  Interest(where: {interest_id: {_eq: "f6e5720a-7285-466f-bc8b-941f0afc673b"}}) {
    title
  }
}

"""
# variables = {"countryCode": "CA"}

# Synchronous request
data = client.execute(query=query,headers=headers)
print(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}



# graphql_url = 'https://innov-8.hasura.app/v1/graphql'
# body = '''
# query MyQuery {
#   Interest(where : {interest_id: {_eq: ""}}) {
#     title
#   }
# }

# '''

# from app.schema import schema 
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
# print(url)
# print(key)
supabase: Client = create_client(url, key)

# def create_app():
#     app.add_url_rule(
#         '/graphql',
#         view_func=GraphQLView.as_view(
#             'graphql',
#             schema=schema,
#             graphiql=True  # for having the GraphiQL interface
#         )
#     )

@app.route('/')
def home():
    # print(url)
    # print(key)
    # data = supabase.table("Student").select("*").execute()
    # response = requests.post(url=url, json={"query": body})
    # print("response status code: ", response.status_code)
    # if response.status_code == 200:
    #     print("response : ", response)
    # Equivalent for SQL Query "SELECT * FROM games;"
    # print(data)
    return render_template('index.html')
