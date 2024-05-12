from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

import hashlib
import random

# Create your models here.
from django.db.models import Q


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    users = models.ManyToManyField(
        User, related_name='rooms', blank=True)
    hash_number = models.CharField(max_length=64, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hash_number

    def name_room(self):
        if len(self.users.all()) == 2:
            self.name = 'Private Chat'
        else:
            self.name = 'Group Chat'
        self.save()

    def rename_room(self, new_name):
        if len(new_name) < 3:
            return

        self.name = new_name
        self.save()

    def generate_hash(self):
        if not self.users.exists():
            return

        if self.hash_number is not None and self.hash_number != '':
            return

        if self.users.count() < 2:
            return

        # Sort user IDs to ensure consistent hash for the same set of participants
        sorted_ids = sorted([str(user.id) for user in self.users.all()])

        # Concatenate the sorted IDs into a single string
        concatenated_ids = '-'.join(sorted_ids)

        if self.users.count() > 2:
            # add a random nonce to the hash to ensure uniqueness
            nonce = str(random.randint(0, 1000000))
            concatenated_ids += '-' + nonce
        # Generate a hash using SHA-256 algorithm
        hash_object = hashlib.sha256(concatenated_ids.encode())

        # Set the hash_number field to the hexadecimal representation of the hash
        self.hash_number = hash_object.hexdigest()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
