from clients import app
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


