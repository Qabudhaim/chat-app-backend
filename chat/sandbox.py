import requests


def main():
    # Define the URL of your Django API endpoint
    url = 'http://localhost:8000/api/check-or-create-room/'

    # Define user IDs for which you want to create or check a chat room
    user1_id = 3
    user2_id = 4

    # Make a POST request to the API endpoint
    response = requests.post(
        url, json={'user1_id': user1_id, 'user2_id': user2_id})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()

        # Display the response data
        print('Room URL:', data['room_url'])
    else:
        print('Failed to create or check room')


if __name__ == '__main__':
    main()
