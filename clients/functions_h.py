from supabase import create_client, Client
from python_graphql_client import GraphqlClient
client = GraphqlClient(endpoint="https://innov-8.hasura.app/v1/graphql")
headers = {
    "x-hasura-admin-secret": "SLZkKBZbyB5qrPgJGM6e4ytxrEgDymSoZ756aSDkf8ky6cDYGRPFrc7D3alyV3fp"}


def userRegister(type, email, password, uuid):
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


def createEvent(name, location, start_date, start_time, end_date, end_time, type, description, uuid):
    type_id = ""
    if type == "Exhibition":
        type_id = "dcd6e6f1-2486-4d72-8a80-3e2778d44ea3"
    elif type == "Seminar":
        type_id = "fded67f3-11b1-4729-a039-a0df3f9fc04a"
    else:
        type_id = "a08ff0ad-9a2e-491c-bb0c-21370629186d"

    query = """
    mutation MyMutation($event_description: String = "", $event_end_date: date = "", $event_end_time: time = "", $event_id: uuid = "", $event_location: String = "", $event_name: String = "", $event_start_date: date = "", $event_start_time: time = "", $event_type_id: uuid = "", $organizer_id: uuid = "") {
        insert_Event(objects: {event_description: $event_description, event_end_date: $event_end_date, event_end_time: $event_end_time, event_location: $event_location, event_name: $event_name, event_start_date: $event_start_date, event_start_time: $event_start_time, event_type_id: $event_type_id, organizer_id: $organizer_id}) {
            returning {
            event_id
            }
        }
    }
    """
    variables = {
        "event_description": description,
        "event_end_date": str(end_date),
        "event_end_time": str(end_time),
        "event_location": location,
        "event_name": name,
        "event_start_date": str(start_date),
        "event_start_time": str(start_time),
        "organizer_id": str(uuid),
        "event_type_id": type_id
    }
    data = client.execute(
        query=query, variables=variables, headers=headers)
    return data


def isOrganizer(uuid):
    query = """
    query MyQuery($_eq: uuid = "") {
        Organizer(where: {organizer_id: {_eq: $_eq}}){
            organizer_id
        }
    }
    """
    variables = {
        "_eq": str(uuid)
    }
    data = client.execute(
        query=query, variables=variables, headers=headers)
    if len(data['data']['Organizer']) > 0:
        return True
    else:
        return False


def getEvents2():
    query = """
    query MyQuery {
        Event {
            event_end_date
            event_description
            event_end_time
            event_id
            event_location
            event_name
            event_start_date
            event_start_time
            organizer_id
            event_type_id
            Organizer {
            organizer_name
            }
        }
    }
    """
    data = client.execute(query=query, headers=headers)
    return data['data']['Event']


def checkRegistration(uuid, eventid):
    query = """
    query MyQuery($_eq: uuid = "", $_eq1: uuid = "") {
        Participants(where: {event_id: {_eq: $_eq}, _and: {student_id: {_eq: $_eq1}}}) {
            participant_id,
            team_id
        }
    }
    """
    variables = {
        "_eq": eventid,
        "_eq1": uuid,
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    return data


def findParticipantByEmail(email):
    query = """
    query MyQuery($_eq: String = "") {
        Student(where: {student_email: {_eq: $_eq}}) {
            student_email
            student_id
            student_name
        }
    }
    """
    variables = {
        "_eq": email,
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    return data


def createTeam(eventID):
    query = """
    mutation MyMutation($event_id: uuid = "") {
        insert_Team_one(object: {event_id: $event_id}) {
            team_id
        }
    }
    """
    variables = {
        "event_id": eventID,
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    return data


def participate(uuid, eventID, teamID):
    query = """
    mutation MyMutation($team_id: uuid = "", $student_id: uuid = "", $event_id: uuid = "") {
        insert_Participants_one(object: {team_id: $team_id, student_id: $student_id, event_id: $event_id}) {
            participant_id
        }
    }
    """
    variables = {
        "team_id": teamID,
        "student_id": str(uuid),
        "event_id": eventID,
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    return data


def teamDetails(teamID):
    query = """
    query MyQuery($_eq: uuid = "") {
        Team(where: {team_id: {_eq: $_eq}}) {
            team_id
            event_id
            Participants {
            student_id
            Student {
                student_email
                student_id
                student_name
            }
            }
        }
    }
    """
    variables = {
        "_eq": teamID
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    # Returns an array of the students present in the team
    return data['data']['Team'][0]['Participants']


def isSubmitted(uuid, eventID):
    query = """
    query MyQuery($_eq: uuid = "", $_eq1: uuid = "") {
        Participants(where: {student_id: {_eq: $_eq}, _and: {event_id: {_eq: $_eq1}}}) {
            team_id
        }
    }
    """
    variables = {
        "_eq": str(uuid),
        "_eq1": str(eventID),
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    teamID = data['data']['Participants'][0]['team_id']

    query = """
    query MyQuery($_eq: uuid = "") {
        ProjectLink(where: {team_id: {_eq: $_eq}}) {
            team_id
            project_id
            Project {
            proj_desc
            proj_drive_link
            proj_id
            proj_images
            proj_rich_text_desc
            proj_title
            }
        }
    }
    """
    variables = {
        "_eq": teamID,
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    # This return the array containing 1 or 0 elements,details of the project
    return data['data']['ProjectLink']


def eventDetails(eventID):
    query = """
    query MyQuery($_eq: uuid = "") {
        Event(where: {event_id: {_eq: $_eq}}) {
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
    variables = {
        "_eq": str(eventID)
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    print(data['data']['Event'])
    return data['data']['Event']


def isProjectSubmitted(teamID):
    query = """
    query MyQuery($_eq: uuid = "") {
        ProjectLink(where: {team_id: {_eq: $_eq}}) {
            project_id
        }
    }
    """
    variables = {
        "_eq": str(teamID)
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    if len(data['data']['ProjectLink']) == 0:
        return False
    else:
        return True


def submitProject(title, description, teamID):
    query = """
    mutation MyMutation($proj_desc: String = "", $proj_drive_link: String = "", $proj_images: String = "", $proj_title: String = "", $proj_rich_text_desc: String = "") {
        insert_Project(objects: {proj_desc: $proj_desc, proj_title: $proj_title}) {
            returning {
            proj_id
            proj_desc
            proj_title
            }
        }
    }
    """
    variables = {
        "proj_desc": description,
        "proj_title": title,
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    projectID = data['data']['insert_Project']['returning'][0]['proj_id']

    query = """
    query MyQuery($_eq: uuid = "") {
        Participants(where: {team_id: {_eq: $_eq}}) {
            student_id
        }
    }
    """
    variables = {
        "_eq": str(teamID)
    }
    res = client.execute(query=query, variables=variables, headers=headers)
    student_ids = res['data']['Participants']
    for studentID in student_ids:
        query = """
        mutation MyMutation($project_id: uuid = "", $student_id: uuid = "", $team_id: uuid = "") {
            insert_ProjectLink_one(object: {project_id: $project_id, student_id: $student_id, team_id: $team_id}) {
                link_id
            }
        }
        """
        variables = {
            "project_id": str(projectID),
            "student_id": str(studentID['student_id']),
            "team_id": str(teamID)
        }
        result = client.execute(
            query=query, variables=variables, headers=headers)
        print(result)


def getProject(projectID):
    query = """
    query MyQuery($_eq: uuid = "") {
        Project(where: {proj_id: {_eq: $_eq}}) {
        proj_desc
        proj_id
        proj_rich_text_desc
        proj_title
        proj_drive_link
        proj_images
        }
    }
    """
    variables = {
        "_eq": str(projectID)
    }
    data = client.execute(query=query, variables=variables, headers=headers)
    actual_data = data['data']['Project']
    return actual_data


getProject('e5e76d66-b2e0-476e-b583-6025797704df')
