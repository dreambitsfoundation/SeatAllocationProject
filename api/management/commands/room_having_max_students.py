from django.core.management.base import BaseCommand, CommandParser
from api.models import Room, Seat
from django.db import transaction
from api.views import get_list_of_class_rooms_with_x_students

class Command(BaseCommand):
    help = "Get the room id having the most active seat allocation."

    def handle(self, *args, **params):
        print(get_list_of_class_rooms_with_x_students(return_only_max=True))
