from django.shortcuts import render

from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


class TokenView(APIView):
    def post(self, request):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)

        return Response({
            'access': str(token.access_token)
        })


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'})

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        email = request.data.get('email', '')
        phone_number = request.data.get('phone_number', '')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'})

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


# add a restricted view for users
@permission_classes([IsAuthenticated])
class WhoAmI(APIView):
    def get(self, request):
        return Response({
            'message': 'You are authenticated',
            'user': UserSerializer(request.user).data
        })


@permission_classes([IsAuthenticated])
class MessagesView(APIView):
    def get(self, request):
        room_hash = request.data.get('room_hash')
        messages = Message.objects.filter(room_hash)
        return Response({
            'messages': messages
        })


@permission_classes([IsAuthenticated])
class ListUsersView(APIView):
    def get(self, request):
        # get all users except the current user and serialize them
        users = User.objects.exclude(id=request.user.id)
        users = UserSerializer(users, many=True).data
        return Response({
            'users': users
        })


@permission_classes([IsAuthenticated])
class ListRoomsView(APIView):
    def get(self, request):
        # get all rooms for the current user
        rooms = ChatRoom.objects.filter(users=request.user)
        rooms = ChatRoomSerializer(rooms, many=True).data
        return Response({
            'rooms': rooms
        })


@permission_classes([IsAuthenticated])
class FilterUsersView(APIView):
    def post(self, request):
        query = request.data.get('query')

        if query == '':
            return Response({
                'users': []
            })

        users = User.objects.filter(
            phone_number__icontains=query) | User.objects.filter(email__icontains=query)

        users = UserSerializer(users, many=True).data
        return Response({
            'users': users
        })


@permission_classes([IsAuthenticated])
class ListRoomsAndLastMessagesView(APIView):
    def get(self, request):
        user = request.user
        rooms = user.rooms.all()
        rooms = ChatRoomSerializer(rooms, many=True).data

        chatRooms = []
        for room in rooms:
            last_message = Message.objects.filter(room=room['id']).last()
            room['last_message'] = last_message.message if last_message else ''
            chatRooms.append(room)

        return Response({
            'rooms': chatRooms
        })


@permission_classes([IsAuthenticated])
class CreateRoomView(APIView):
    def post(self, request):
        users = request.data.get('users', [])

        if request.user.id not in users:
            users.append(request.user.id)
        users = User.objects.filter(id__in=users)

        if len(users) < 2:
            return Response({
                'error': 'Select at least 2 users'
            })


        # if the users count equals 2, check if the room already exists
        if len(users) == 2:
            room = ChatRoom.objects.filter(
                users=users[0]).filter(users=users[1])

            if room.exists():
                return Response({
                    'room': ChatRoomSerializer(room.first()).data
                })

        # pass users when creating a room
        room = ChatRoom.objects.create()
        room.save()
        room.users.add(*users)
        room.generate_hash()
        room.save()

        return Response({
            'room': ChatRoomSerializer(room).data
        })


@ permission_classes([IsAuthenticated])
class GetRoomUrlView(APIView):
    def get(self, request):
        room_hash = request.data.get('room_hash')
        room = ChatRoom.objects.get(hash_number=room_hash)
        return Response({
            'url': f'/chat/{room_hash}'
        })


@ permission_classes([IsAuthenticated])
class GetMessagesView(APIView):
    def post(self, request):
        room_hash = request.data.get('room_hash')

        user = request.user
        room = user.rooms.filter(hash_number=room_hash).first()
        messages = Message.objects.filter(room=room)
        messages = MessageSerializer(messages, many=True).data

        return Response({
            'messages': messages
        })


@ permission_classes([IsAuthenticated])
class SendMessageView(APIView):
    def post(self, request):
        room_hash = request.data.get('room_hash')
        message = request.data.get('message')

        user = request.user
        room = user.rooms.filter(hash_number=room_hash).first()

        if room is None:
            return Response({
                'error': 'Room not found'
            })

        message = Message.objects.create(
            user=user, room=room, message=message)
        message.save()

        return Response({
            'message': MessageSerializer(message).data
        })


@ permission_classes([IsAuthenticated])
class LastMessagesView(APIView):
    def get(self, request):
        user = request.user
        rooms = user.rooms.all()
        last_messages = {}
        for room in rooms:
            last_message = Message.objects.filter(room=room).last()
            last_messages[room.hash_number] = last_message.message if last_message else [
            ]

        return Response({
            'last_messages': last_messages
        })
