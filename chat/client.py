import requests
import json


def login(username, password):
    url = 'http://localhost:8000/login/'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=data)
    return response.json()


def register(username, password, first_name, last_name, email, phone_number):
    url = 'http://localhost:8000/register/'
    data = {
        'username': username,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone_number': phone_number
    }

    response = requests.post(url, data=data)
    return response.json()


def who_am_i(access_token):
    url = 'http://localhost:8000/whoami/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def list_users(access_token):
    url = 'http://localhost:8000/api/list-users/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def filter_users(access_token, query):
    url = 'http://localhost:8000/api/filter-users/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'query': query
    }

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    return response.json()


def list_rooms(access_token):
    url = 'http://localhost:8000/api/list-rooms/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def create_room(access_token, users):
    url = 'http://localhost:8000/api/create-room/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'users': users
    }

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    return response.json()


def get_messages(access_token, room_hash):
    url = 'http://localhost:8000/api/messages/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'room_hash': room_hash
    }

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    return response.json()


def send_message(access_token, room_hash, message):
    url = 'http://localhost:8000/api/send-message/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'room_hash': room_hash,
        'message': message
    }

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    return response.json()


def last_messages(access_token):
    url = 'http://localhost:8000/api/last-messages/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def list_rooms_and_messages(access_token):
    url = 'http://localhost:8000/api/list-rooms-and-messages/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_jwt_token(username, password):
    url = 'http://localhost:8000/api/token/'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=data)
    return response.json()


def get_refresh_token(refresh_token):
    url = 'http://localhost:8000/api/token/refresh/'
    data = {
        'refresh': refresh_token
    }
    response = requests.post(url, data=data)
    return response.json()


def get_access_token(refresh_token):
    url = 'http://localhost:8000/get-token/'
    data = {
        'refresh': refresh_token
    }
    response = requests.post(url, data=data)
    return response.json()


# response = register('Emad', 'Emad123456789')
# print(response)

# response = login('Emad', 'Emad123456789')
# print(response)

# access_token = response['access']
# refresh_token = response['refresh']

# response = who_am_i(access_token)
# print(response)

# response = register('Lamis', 'Lamis123456789', 'Lamis',
#                     '', '', '')
# print(response)

response = login('Lamis', 'Lamis123456789')
access_token = response['access']
refresh_token = response['refresh']

print(access_token)
# access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1NDU0Mzg5LCJpYXQiOjE3MTUzNjc5ODksImp0aSI6IjM3NjJjYjQ4MDYwZDRlMmQ5MGI2MjJlNzQ3NDgwMjBkIiwidXNlcl9pZCI6M30.fc72xadiRTKZQxJaPgy3s-eflGi-mwyN3JUNFMGYtl4'
response = who_am_i(access_token)
print(response)

# response = send_message(
#     access_token, '1ba709d2440f09ecbfe6754a83ce9e22e51146297ac904d002d5ba01645fa6ed', 'Hello')
# print(response)

# response = get_messages(
#     access_token, '1ba709d2440f09ecbfe6754a83ce9e22e51146297ac904d002d5ba01645fa6ed')
# print(response)

# response = create_room(access_token, [3])
# print(response)
