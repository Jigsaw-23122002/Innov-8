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
from clients import mde
from clients.forms import CreateEventForm, CreateProjectForm, EventRegistration, LoginForm, SignUpForm, redirectCreateProject
import markdown
from clients.functions_h import createTeam, eventDetails, isOrganizer, isProjectSubmitted, isSubmitted, participate, submitProject, teamDetails, userRegister, createEvent, isOrganizer, getEvents, checkRegistration, findParticipantByEmail
from clients.forms import LoginForm, SignUpForm, MessageForm


# from app.schema import schema
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)
if (supabase.auth.current_user):
    user = supabase.auth.current_user.id
else:
    user = -1
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
  query MyQuery($_eq: uuid = "") {
    Student(where: {student_name: {_eq: ""}}) {
      student_email
      student_id
      student_name
      student_password
    }
  }
  """
  variables = {
    "_eq": userId
  }
  data = client.execute(query=query, headers=headers, variables=variables)['data']['Student']
  return data


def userDetails():
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
    variables = {
        "sponsor_id": user,
        "event_id": id
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
    data = client.execute(query=query, headers=headers)
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


def sendMessage(to_id, msg):
    query = """
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
    query = """
  query MyQuery {
    Organizer {
      organizer_email
      organizer_id
      organizer_name
      organizer_password
    }
  }
  """
    data = client.execute(query=query, headers=headers)
    return data
    # conn=db_connection()
    # cursor=conn.cursor()
    # sql_query = '''
    # SELECT * FROM Organizer '''
    # cursor =cursor.execute(sql_query)
    # return cursor.fetchall()


@app.route('/')
def home_page():
    if supabase.auth.current_user:
        print(supabase.auth.current_user.id)
    else:
        print('null')
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')
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



@app.route('/studentList')
def studentList():
  data = getStudentList()
  folowerList =[]
  for stud in data:
    print("id of student:",stud['student_id'])
    folowerList.append(isFollowed(stud['student_id'])) 
  return render_template('students_list.html', data = data, folowerList = folowerList,size = len(data))

@app.route('/displayProjects/<int:pId>')
def displayProjects(pId):
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
        "proj_id": {"_eq": pId}
    }
    data = client.execute(query=query, headers=headers, variables=variables)
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


@app.route('/logout')
def logout():
    supabase.auth.sign_out()
    return redirect('/')


@app.route('/create_project/<teamID>', methods=['GET', 'POST'])
def create_project(teamID):
    if isProjectSubmitted(teamID) == False:
        form = CreateProjectForm()
        if form.validate_on_submit():
            html = markdown.markdown(
                form.description.data,
                extensions=['nl2br', 'smarty', 'pymdownx.tilde', 'extra']
            )
            submitProject(form.name.data, form.description.data, teamID)
            return redirect('/events')
        return render_template('create_project.html', form=form, mde=mde)
    else:
      return redirect('error')
      


@app.route('/error')
def error():
    return render_template('404.html')


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if supabase.auth.current_user:
        if isOrganizer(supabase.auth.current_user.id):
            form = CreateEventForm()
            if form.validate_on_submit():
                data = createEvent(form.name.data, form.location.data, form.start_date.data, form.start_time.data,
                                   form.end_date.data, form.end_time.data, form.type.data, form.description.data, supabase.auth.current_user.id)
            return render_template('create_event.html', form=form)
        else:
            return redirect('/error')
    else:
        return redirect('/error')


@app.route('/events')
def events():
    data = getEvents()
    return render_template('events.html', data=data)


@app.route('/register/<eventID>', methods=['GET', 'POST'])
def register(eventID):
    data = checkRegistration(str(supabase.auth.current_user.id), str(eventID))
    if len(data['data']['Participants']) > 0:
        teamID = data['data']['Participants'][0]['team_id']
        event_details = eventDetails(str(eventID))
        team_details = teamDetails(str(teamID))
        form = redirectCreateProject()

        if form.validate_on_submit():
            return redirect(f'/create_project/{str(teamID)}')

        return render_template('team_event.html', event_details=event_details, team_details=team_details, form=form)

    else:
        form = EventRegistration()
        if form.validate_on_submit():
            participants = [str(supabase.auth.current_user.id)]

            res = findParticipantByEmail(form.email_01.data)
            if len(res['data']['Student']) > 0 and len(checkRegistration(res['data']['Student'][0]['student_id'], eventID)['data']['Participants']) == 0:
                participants.append(res['data']['Student'][0]['student_id'])

            res = findParticipantByEmail(form.email_02.data)
            if len(res['data']['Student']) > 0 and len(checkRegistration(res['data']['Student'][0]['student_id'], eventID)['data']['Participants']) == 0:
                participants.append(res['data']['Student'][0]['student_id'])

            res = findParticipantByEmail(form.email_03.data)
            if len(res['data']['Student']) > 0 and len(checkRegistration(res['data']['Student'][0]['student_id'], eventID)['data']['Participants']) == 0:
                participants.append(res['data']['Student'][0]['student_id'])

            print(participants)
            teamID = createTeam(eventID)
            print(teamID)
            for uuid in participants:
                ress = participate(str(uuid), eventID, str(
                    teamID['data']['insert_Team_one']['team_id']))
                print(ress)

        return render_template('register_for_event.html', form=form)
