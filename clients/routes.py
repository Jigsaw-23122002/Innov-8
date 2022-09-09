import os
from pydoc import cli
from flask import redirect, render_template,flash,request
from flask import Flask
from clients import app
from flask_sqlalchemy import SQLAlchemy
from supabase import create_client, Client
# from flask_graphql import GraphQLView
from python_graphql_client import GraphqlClient
# import requests



# from app.schema import schema 
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)
user = supabase.auth.user()
# print(user)

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://innov-8.hasura.app/v1/graphql")
headers = { "x-hasura-admin-secret": "SLZkKBZbyB5qrPgJGM6e4ytxrEgDymSoZ756aSDkf8ky6cDYGRPFrc7D3alyV3fp" }
# Create the query string and variables required for the request.
# variables = {"countryCode": "CA"}
  

def organizerDetail():
  query = """
  query MyQuery {
    Organizer {
      organizer_email
      organizer_id
      organizer_name
    }
  }
  """
  data = client.execute(query=query,headers=headers)
  print(data) # {'data': {'Organizer': []}}
# organizerDetail()

def searchProject(ProjectTitle):
  query = """
  query MyQuery($proj_title: String_comparison_exp = {_eq: ""}) {
    Project(where: {proj_title: $proj_title}) {
      proj_id
      proj_title
      proj_rich_text_desc
      proj_desc
      proj_drive_link
    }
  }
  """
  variables = {
    "proj_title": {"_eq":ProjectTitle}
  }
  data = client.execute(query = query, headers = headers,variables=variables)
  return data # {'data': {'Project': [{'proj_id': 'ed523569-35f9-4651-a44c-2f00b8717b35', 'proj_title': 'Ananya', 'proj_rich_text_desc': 'bkfebfkj', 'proj_desc': 'dbkewbfkw', 'proj_drive_link': 'fhwjbfkwejfbhr'}]}}

print(searchProject("Ani")['data']['Project']==[])
def getProjectList(usr_det):
  query = """
  query MyQuery($student_id: uuid_comparison_exp = {}) {
    ProjectLink(where: {student_id: $student_id}) {
      link_id
      project_id
      student_id
    }
  }
  """
  variables = {
    "student_id": {"_eq": usr_det}
  }
  projLinkDet=client.execute(query=query,variables=variables,headers=headers)
  if projLinkDet['data']['ProjectLink']==[]:
      return []
  query = """
  query MyQuery($proj_id: uuid_comparison_exp = {}) {
    Project(where: {proj_id: $proj_id}) {
      proj_desc
      proj_drive_link
      proj_id
      proj_rich_text_desc
      proj_title
    }
  }  
  """
  variables = {
    "proj_id": {"_eq": projLinkDet['data']['ProjectLink'][0]['project_id']}
  }
  data = client.execute(query = query, variables=variables,headers = headers)
  return data

def FollowUser(usr_det):
  query="""
  mutation MyMutation($follower_id: uuid = "", $following_id: uuid = "") {
    insert_Follow_one(object: {follower_id: $follower_id, following_id: $following_id}) {
      follow_id
    }
  }  
  """
  variables = {
    "follower_id": usr_det,
    "following_id": user
  }
  data = client.execute(query = query, variables=variables,headers = headers)
  return data
  # conn = db_connection()
  # cursor = conn.cursor()
  # usr_id = userDetails()[0][0]
  # # tou=current_user.type_of_user
  # sql_query = '''INSERT into Follow(follower_id,following_id) values ({},{})'''.format( usr_det[0][0], usr_id)
  # cursor =cursor.execute(sql_query)
  # conn.commit()


def isFollowed(usr_det):
  query = """
  query MyQuery($follower_id: uuid_comparison_exp = {}, $following_id: uuid_comparison_exp = {}) {
    Follow(where: {follower_id: $follower_id, following_id: $following_id}) {
      follow_id
    }
  }
  """
  variables = {
    "follower_id": {"_eq": usr_det},
    "following_id": {"_eq": user} 
  }
  data = client.execute(query = query, variables=variables,headers = headers)
  return data['data']['Follow']==[]

def isSponsored():
  conn = db_connection()
  cursor = conn.cursor()
  usr_id = userDetails()[0][0]
  query = """
  query MyQuery($sponsor_id: uuid_comparison_exp = {}) {
    Sponsorship(where: {sponsor_id: $sponsor_id}) {
      event_id
    }
  }
  """
  variables = {
    "sponsor_id": {"_eq": ""}
  }
  data = client.execute(query = query, variables=variables,headers = headers)
  return data

def getEvents():
  query = """
  query MyQuery {
    Event {
      event_description
      event_end_date
      event_id
      event_location
      event_type_id
      organizer_id
      team_id
      event_start_date
    }
  }
  """
  data = client.execute(query = query,headers=headers)
  return data

def searchOrganizer(userId):
  query = """
  query MyQuery($organizer_id: uuid_comparison_exp = {}) {
    Organizer(where: {organizer_id: $organizer_id}) {
      organizer_email
      organizer_id
      organizer_name
      organizer_password
    }
  }
  """
  variables = {
    "organizer_id": {
      "_eq": userId
    }
  }
  data = client.execute(query = query,headers=headers,variables=variables)
  return data 

def searchSponsor(userId):
  query = """
  query MyQuery($sponsor_id: uuid_comparison_exp = {}) {
    Sponsor(where: {sponsor_id: $sponsor_id}) {
      sponsor_email
      sponsor_id
      sponsor_interests
      sponsor_name
      sponsor_password
      sponsorship_tier
    }
  }
  """
  variables = {
    "sponsor_id": {
      "_eq": userId
    }
  }
  data = client.execute(query = query,headers=headers,variables=variables)
  return data

def searchStudent(userId):
  query = """
  query MyQuery($student_id: uuid_comparison_exp = {}) {
    Student(where: {student_id: $student_id}) {
      student_email
      student_id
      student_name
      student_password
    }
  }
  """
  variables = {
    "student_id": {
      "_eq": userId
    }
  }
  data = client.execute(query = query,headers=headers,variables=variables)
  return data

def userDetails():
  data = searchOrganizer(user)
  if(data["data"]["Organizer"]!=[]):
    return data
  data = searchSponsor(user)
  if(data["data"]["Sponsor"]!=[]):
    return data
  data = searchStudent(user)
  if(data["data"]["Student"]!=[]):
    return data
  return []

def getUserList(typeofuser,Searchuser):
  if(typeofuser=="Student"):
    return searchStudent(Searchuser)
  if(typeofuser=="Sponsor"):
    return searchSponsor(Searchuser)
  if(typeofuser=="Organizer"):
    return searchOrganizer(Searchuser)
  return []
  # conn = db_connection()
  # cursor = conn.cursor()
  # # tou=current_user.type_of_user
  # tou=typeofuser
  # sql_query = '''
  # SELECT * FROM {} WHERE {} = "{}"'''.format(table_info[tou][0],table_info[tou][1],Searchuser)
  # cursor =cursor.execute(sql_query)
  
  # return cursor.fetchall()

def getSponsorship(id):
  query = """
  mutation MyMutation($event_id: uuid = "", $sponsor_id: uuid = "") {
    insert_Sponsorship(objects: {event_id: $event_id, sponsor_id: $sponsor_id}) {
      returning {
        sponsorer_id
      }
    }
  }
  """
  variables  = {
    "sponsor_id": user,
    "event_id": id
  }
  data  = client.execute(query=query, variables=variables,headers=headers)
  return data

def getSponsorsList():
  query = """
  query MyQuery {
    Sponsor {
      sponsor_email
      sponsor_id
      sponsor_interests
      sponsor_name
      sponsor_password
      sponsorship_tier
    }
  }
  """
  data  = client.execute(query=query,headers=headers)
  return data

def getStudentList():
  query = """
  query MyQuery {
    Student {
      student_email
      student_id
      student_name
      student_password
    }
  }
  """
  data  = client.execute(query=query,headers=headers)
  return data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/posts')
def posts():
  return render_template('posts.html') 
