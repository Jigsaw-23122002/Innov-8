
import email
import os
from pydoc import cli
from winreg import QueryInfoKey
from flask import redirect, render_template, flash, request
from flask import Flask
from flask import url_for
from clients import app
from flask_sqlalchemy import SQLAlchemy
from supabase import create_client, Client
from python_graphql_client import GraphqlClient
from urllib import request
from clients.forms import EditProfile, LoginForm, SearchForm, SignUpForm, MessageForm, SponsorshipForm


# from app.schema import schema
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)
# if(supabase.auth.current_user):
#   user = supabase.auth.current_user.id
# else:
#   user = -1
# print(user)

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://innov-8.hasura.app/v1/graphql")
headers = {
    "x-hasura-admin-secret": "SLZkKBZbyB5qrPgJGM6e4ytxrEgDymSoZ756aSDkf8ky6cDYGRPFrc7D3alyV3fp"}
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
    data = client.execute(query=query, headers=headers)
    print(data)  # {'data': {'Organizer': []}}
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
        "proj_title": {"_eq": ProjectTitle}
    }
    data = client.execute(query=query, headers=headers, variables=variables)
    # {'data': {'Project': [{'proj_id': 'ed523569-35f9-4651-a44c-2f00b8717b35', 'proj_title': 'Ananya', 'proj_rich_text_desc': 'bkfebfkj', 'proj_desc': 'dbkewbfkw', 'proj_drive_link': 'fhwjbfkwejfbhr'}]}}
    return data


print(searchProject("Ani")['data']['Project'] == [])


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
    projLinkDet = client.execute(
        query=query, variables=variables, headers=headers)
    if projLinkDet['data']['ProjectLink'] == []:
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
    data = client.execute(query=query, variables=variables, headers=headers)
    return data


def FollowUser(usr_det):
    query = """
  mutation MyMutation($follower_id: uuid = "", $following_id: uuid = "") {
    insert_Follow_one(object: {follower_id: $follower_id, following_id: $following_id}) {
      follow_id
    }
  }  
  """
    user = supabase.auth.current_user.id
    print("required data is :",user,usr_det)
    variables = {
        "follower_id": str(usr_det),
        "following_id": str(user)
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    print("req data is",data)
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
  # print(supabase.auth.current_user)
  user = supabase.auth.current_user.id
  variables = {
      "follower_id": {"_eq": str(usr_det)},
      "following_id": {"_eq": str(user)}
  }
  print("id of user",user)
  data = client.execute(query=query, variables=variables, headers=headers)
  print("data of the page is",data)
  return data['data']['Follow'] != []


def isSponsored():
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
    data = client.execute(query=query, variables=variables, headers=headers)
    return data


def getEvents():
  query = """
  query MyQuery {
    Event {
      event_description
      event_end_date
      event_end_time
      event_id
      event_location
      event_name
      event_start_date
      event_start_time
      event_type_id
      organizer_id
    }
  }

  """
  data = client.execute(query=query, headers=headers)
  return data['data']['Event']


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
    data = client.execute(query=query, headers=headers, variables=variables)
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
    data = client.execute(query=query, headers=headers, variables=variables)
    return data


def searchStudent(userId):
  query = """
  query MyQuery($_like: String = "") {
    Student(where: {student_name: {_like: $_like}}) {
      student_email
      student_id
      student_name
      student_password
    }
  }
  """
  userId = "%" + userId + "%"
  variables = {
    "_like": userId
  }
  
  data = client.execute(query=query, headers=headers, variables=variables)
  print("Mydata is",data)
  return data['data']['Student']


def userDetails():
  user = supabase.auth.current_user.id
  data = searchOrganizer(user)
  if (data["data"]["Organizer"] != []):
      return data
  data = searchSponsor(user)
  if (data["data"]["Sponsor"] != []):
      return data
  data = searchStudent(user)
  if (data["data"]["Student"] != []):
      return data
  return []


def getUserList(typeofuser, Searchuser):
    if (typeofuser == "Student"):
        return searchStudent(Searchuser)
    if (typeofuser == "Sponsor"):
        return searchSponsor(Searchuser)
    if (typeofuser == "Organizer"):
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
  user = supabase.auth.current_user.id
  variables = {
      "sponsor_id": str(user),
      "event_id": str(id)
  }
  data = client.execute(query=query, variables=variables, headers=headers)
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
    data = client.execute(query=query, headers=headers)['data']['Sponsor']
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
    data = client.execute(query=query, headers=headers)
    return data["data"]["Student"]


def userRegister(type, email, password, uuid):
    print(type)
    print(email)
    print(password)
    print(uuid)
    if type == 'Student':
        query = """
        mutation MyMutation($student_id: uuid = "", $student_email: String = "", $student_password: String = "") {
          insert_Student_one(object: {student_id: $student_id, student_email: $student_email, student_password: $student_password}) {
            student_id
          }
        }
        """
        variables = {
            "student_email": email,
            "student_id": str(uuid),
            "student_password": password
        }
        data = client.execute(
            query=query, variables=variables, headers=headers)
        print(data)
        return data

    elif type == 'Organizer':
        query = """
        mutation MyMutation($organizer_id: uuid = "", $organizer_email: String = "", $organizer_password: String = "") {
          insert_Organizer_one(object: {organizer_id: $organizer_id, organizer_email: $organizer_email, organizer_password: $organizer_password}) {
            organizer_id
          }
        }
        """
        variables = {
            "organizer_email": email,
            "organizer_id": str(uuid),
            "organizer_password": password,
        }
        data = client.execute(
            query=query, variables=variables, headers=headers)
        return data

    else:
        query = """
        mutation MyMutation($sponsor_id: uuid = "", $sponsor_email: String = "", $sponsor_password: String = "") {
          insert_Sponsor_one(object: {sponsor_id: $sponsor_id, sponsor_email: $sponsor_email, sponsor_password: $sponsor_password}) {
            sponsor_id
          }
        }
        """
        variables = {
            "sponsor_email": email,
            "sponsor_id": str(uuid),
            "sponsor_password": password,
        }
        data = client.execute(
            query=query, variables=variables, headers=headers)
        return data

def sendMessage(to_id,msg):
  query ="""
  mutation MyMutation($to_id: uuid = "", $user_id: uuid = "", $user_msg: String = "") {
    insert_Message(objects: {to_id: $to_id, user_id: $user_id, user_msg: $user_msg}) {
      returning {
        message_id
      }
    }
  } 
  
  """
  user =  supabase.auth.current_user.id
  variables = {
    "to_id": str(to_id),
    "user_id": str(user),
    "user_msg": msg
  }
  data = client.execute(variables=variables,query=query,headers=headers)
  return data
  # conn = db_connection()
  # cursor = conn.cursor()
  # usr_id = userDetails()[0][0]
  # # tou=current_user.type_of_user

  # sql_query = '''INSERT into Message(user_id,user_msg ,to_id) values ({},"{}",{})'''.format(usr_id,msg,to_id)
  # print(sql_query)
  # cursor =cursor.execute(sql_query)
  # conn.commit()   

def myFunc(e):
  return e['time']

def getMessage(to_id):
  query = """
  query MyQuery($_eq: uuid = "", $_eq1: uuid = "") {
    Message(where: {to_id: {_eq: $_eq}, user_id: {_eq: $_eq1}}) {
      message_id
      time
      to_id
      user_id
      user_msg
    }
  }
  """
  user = supabase.auth.current_user.id
  variables = {
    "_eq": str(to_id),
    "_eq1": str(user)
  }
  data = client.execute(query = query, variables = variables, headers = headers)["data"]["Message"]
  query = """
  query MyQuery($_eq: uuid = "", $_eq1: uuid = "") {
    Message(where: {to_id: {_eq: $_eq}, user_id: {_eq: $_eq1}}) {
      message_id
      time
      to_id
      user_id
      user_msg
    }
  }
  """
  variables = {
    "_eq": str(user),
    "_eq1": str(to_id)
  }
  data2 = client.execute(query = query, variables = variables, headers = headers)["data"]["Message"]
  newData = data + data2
  newData.sort(key = myFunc)
  print(newData)
  return newData  



def getOrganizerList():
  query ="""
  query MyQuery {
    Organizer {
      organizer_email
      organizer_id
      organizer_name
      organizer_password
    }
  }
  """
  data = client.execute(query = query,headers=headers)
  return data
  # conn=db_connection()
  # cursor=conn.cursor()
  # sql_query = '''
  # SELECT * FROM Organizer '''
  # cursor =cursor.execute(sql_query)
  # return cursor.fetchall()

def listofUsersFollowed():
  query = """
  query MyQuery($_eq: uuid = "") {
    Follow(where: {following_id: {_eq: $_eq}}) {
      follower_id
    }
  }
  """
  variables = {
    "_eq": str(supabase.auth.current_user.id)
  }
  data = client.execute(query = query,variables=variables,headers=headers)['data']['Follow']
  return data

def getStudDetails(id_user):
  query = """
  query MyQuery($_eq: uuid = "") {
    Student(where: {student_id: {_eq: $_eq}}) {
      student_bio
      student_email
      student_id
      student_interest
      student_name
      student_password
    }
  }
  """
  variables = {
    "_eq": str(id_user)
  }
  data = client.execute(query = query,variables=variables,headers=headers)['data']['Student']
  return data

@app.route('/timeline')
def timeline():
  det = []
  user_detail = dict()
  i=0
  for usr in listofUsersFollowed():
    newdet = listOfProjectList(usr['follower_id'])
    det = det + newdet
    for j in range(0,len(newdet)):
      user_detail[i] = (getStudDetails(usr['follower_id'])[0]['student_name'])
      i = i+1
  return render_template('posts.html',det=det,user_detail=user_detail,size = len(det))

@app.route('/')
def home_page():
    if supabase.auth.current_user:
        print(supabase.auth.current_user.id)
    else:
        print('null')
    return render_template('index.html')

def getListOfSponsoredEvents():
  query = """
  query MyQuery($_eq: uuid = "") {
    Sponsorship(where: {sponsor_id: {_eq: $_eq}}) {
      event_id
    }
  }
  """
  user = supabase.auth.current_user.id
  variables = {
    "_eq": str(user)
  }
  data = client.execute(query = query ,variables=variables , headers = headers)['data']['Sponsorship']
  dataList =[]
  for dd in data:
    dataList.append(dd['event_id'])
  return dataList

@app.route('/listOfSponsors')
def listOfSponsors():
  events = getEvents()
  form = SponsorshipForm()
  sponsorsList = []
  dataList = getListOfSponsoredEvents()
  for event in events:
    sponsorsList.append(event['event_id'] in dataList)
  return render_template('events_for_sponsors.html',sponsorsList=sponsorsList,events = events, size = len(events),form = form)

@app.route('/availSponsorship/<eventId>',methods=['GET','POST'])
def availSponsorship(eventId):
  form = SponsorshipForm()
  events = getEvents()
  getSponsorship(events[int(eventId)]['event_id'])
  return redirect('/listOfSponsors')

def listOfProjectList(userid):
  query = """
  query MyQuery($_eq: uuid = "") {
    ProjectLink(where: {student_id: {_eq: $_eq}}) {
      Project {
        proj_desc
        proj_drive_link
        proj_id
        proj_rich_text_desc
        proj_title
      }
    }
  }
  """
  user = supabase.auth.current_user.id
  variables = {
    "_eq": str(userid)
  }
  data = client.execute(query=query,variables=variables,headers=headers)
  return data['data']['ProjectLink']


@app.route('/followUser/<user_det>')
def followUser(user_det):
  FollowUser(user_det)
  return redirect('/studentList')

@app.route('/chat/<user_det>')
def chat(user_det):
  messageList = getMessage(user_det) 
  userList = []
  user = supabase.auth.current_user.id
  for msg in messageList:
    userList.append(str(msg["user_id"])==str(user))
  form = MessageForm()
  return render_template('chat.html',userList=userList ,data = messageList,size = len(messageList),user_det=user_det, form =form)

@app.route('/addMsg/<user_det>',methods=['GET','POST'])
def addMsg(user_det):
  form  = MessageForm()
  message = form.message.data
  data2 = sendMessage(user_det,message)
  return redirect(url_for('chat',user_det = user_det))

def getUserDetailForProile():
  user = supabase.auth.current_user.id
  query = """
  query MyQuery($_eq: uuid = "") {
    Student(where: {student_id: {_eq: $_eq}}) {
      student_email
      student_id
      student_name
      student_password
      student_bio
      student_interest
    }
  }
  """ 
  variables = {
    "_eq": str(user)
  }
  data = client.execute(query=query,headers = headers,variables=variables)['data']['Student']
  return data

def followerCount():
  query = """
  query MyQuery($_eq: uuid = "") {
    Follow_aggregate(where: {follower_id: {_eq: $_eq}}) {
      aggregate {
        count(columns: follow_id)
      }
    }
  }
  """
  user = supabase.auth.current_user.id
  variables = {
    "_eq": str(user)
  }
  data = client.execute(query=query,headers = headers,variables=variables)['data']['Follow_aggregate']['aggregate']['count']
  query = """
  query MyQuery($_eq: uuid = "") {
    Follow_aggregate(where: {following_id: {_eq: $_eq}}) {
      aggregate {
        count(columns: follow_id)
      }
    }
  }
  """
  user = supabase.auth.current_user.id
  variables = {
    "_eq": str(user)
  }
  data2 = client.execute(query=query,headers = headers,variables=variables)['data']['Follow_aggregate']['aggregate']['count']
  return [data,data2]

@app.route('/profilePage')
def profilePage():
  details = getUserDetailForProile()[0]
  projectList = listOfProjectList(supabase.auth.current_user.id)
  follower = followerCount()[0]
  following = followerCount()[1]
  projectsCount = len(projectList)
  return render_template('profile.html',details=details,projectList = projectList,follower = follower,following=following,projectsCount=projectsCount)

@app.route('/editprofilePage')
def editprofilePage():
  form = EditProfile()
  return render_template('edit_profile.html', form = form)

def changeStdDetails(bio_info,name_info,email_info,interest_info):
  query = """
  mutation MyMutation($_eq: uuid = "", $student_bio: String = "", $student_email: String = "", $student_interest: String = "", $student_name: String = "") {
    update_Student(where: {student_id: {_eq: $_eq}}, _set: {student_bio: $student_bio, student_email: $student_email, student_interest: $student_interest, student_name: $student_name}) {
      returning {
        student_id
      }
    }
  }
  """
  user = supabase.auth.current_user.id
  variables = {
    "_eq": str(user),
    "student_bio": str(bio_info),
    "student_name": str(name_info),
    "student_email": str(email_info),
    "student_interest": str(interest_info)
  }
  data = client.execute(query = query, variables = variables,headers=headers)


@app.route('/editProfileHelper',methods=['GET','POST'])
def editProfileHelper():
  form = EditProfile()
  changeStdDetails(form.bio.data,form.fName.data,form.email.data,form.interest.data)
  return redirect('/editprofilePage')

@app.route('/studentList')
def studentList():
  data = getStudentList()
  form  = SearchForm()
  folowerList =[]
  for stud in data:
    print("id of student:",stud['student_id'])
    folowerList.append(isFollowed(stud['student_id'])) 
  return render_template('students_list.html', data = data, folowerList = folowerList,size = len(data),form = form)

@app.route('/searchStud',methods=['GET','POST'])
def searchStud():
  form = SearchForm()
  searchStudentName = form.messageText.data
  print('student name is',searchStudentName)
  data = searchStudent(searchStudentName)
  print('student data in search  is',data)
  folowerList =[]
  for stud in data:
    print("id of student:",stud['student_id'])
    folowerList.append(isFollowed(stud['student_id'])) 
  return render_template('students_list.html', data = data, folowerList = folowerList,size = len(data),form = form)

@app.route('/displayProjects/<int:pId>')
def displayProjects(pId):
  query ="""
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
    "proj_id": {"_eq": pId}
  }
  data = client.execute(query = query, headers = headers,variables=variables)
  print(data)
  # return render_template('list_of_projects.html', prjDetails= data["data"]["Project"],stdID = user)
    # conn=db_connection()
    # cursor=conn.cursor()
    # sql_query ='''
    # SELECT * FROM Project where project_id = {}
    # '''.format(pId)
    # cursor=cursor.execute(sql_query)
    # formNew=SearchUserForm()
    # prjDetails=cursor.fetchall()
    # stdID=userDetails()[0][1]
    # return render_template('project_revamp.html', prjDetails=prjDetails, stdID=stdID, formNew=formNew)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            random_email: str = form.email.data
            random_password: str = form.password.data
            user = supabase.auth.sign_up(
                email=random_email, password=random_password)
            userRegister(form.category.data, random_email,
                         random_password, user.id)
            if supabase.auth.current_user:
                print(supabase.auth.current_user.id)
            else:
                print('null')
            return redirect('/login')

        except ValueError as e:
            print('An exception occured')

    if form.errors != {}:
        for err in form.errors.values():
            flash(
                f'there was an error in creating a user:{err}', category="danger")

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            random_email: str = form.email.data
            random_password: str = form.password.data
            user = supabase.auth.sign_in(
                email=random_email, password=random_password)
            print(supabase.auth.current_user.id)
            return redirect('/')

        except ValueError as e:
            print(e)

    return render_template('login.html', form=form)


@app.route('/individual_projects')
def individual_projects():
    # Fetch the projects made the uuid of the student who is signed in
    data = [{
        'project_uuid': 'lambda',
        'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }
            ]
    return render_template('individual_projects.html', data=data)


@app.route('/individual_events')
def individual_events():
    # Fetch the projects made the uuid of the organizer who is signed in
    data = [{
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }]
    return render_template('individual_events.html', data=data)


@app.route('/list_projects')
def list_projects():
    # Fetch the list of projects for the particular event
    data = [{
        'project_uuid': 'lambda',
        'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }, {
            'project_uuid': 'lambda',
            'team_name': 'TechnoSrats',
            'team_members': [
                'Harsh Nag',
                'Sarvagnya Purohit',
                'Ketaki Deshmukh',
                'Smit Sekhadia',
                'Anuraag Jajoo'
            ],
            'project_description':'This template offers an outline to create an architectural or construction project description template. Customize the template based on the type of project and the needs of your company or client. List supporting documents, such as environmental analysis or additional design plans. Follow the template format to create a thorough project description that includes goals, phases, design specifications, and financial requirements.'
            }
            ]
    return render_template('list_of_projects.html', data=data)


@app.route('/list_events')
def list_events():
    # Fetch the list of events available for participation
    data = [{
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }, {
        'event_uuid': 'sunderbans',
        'event_name': 'HackOdisha 2.0',
        'event_sponsorers': [
            'Amazon',
            'Flipkart',
            'Firebase'
        ],
        'event_description':'An event description is copy that aims to tell your potential attendees what will be happening at the event, who will be speaking, and what they will get out of attending. Good event descriptions can drive attendance to events and also lead to more media coverage.',
    }]
    return render_template('list_of_events.html', data=data)


@app.route('/logout')
def logout():
    supabase.auth.sign_out()
    return redirect('/')
