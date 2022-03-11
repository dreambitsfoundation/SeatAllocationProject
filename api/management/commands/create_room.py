from django.core.management.base import BaseCommand, CommandParser
from api.models import Room, Seat
from django.db import transaction

class Command(BaseCommand):
    help = "This command is used to create new room with a number as seats."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('name', type=str, help="Name of the room 10-characters max")
        parser.add_argument('--seat_capacity', type=int, help="Number of seats that is to be added (default is 15)", default=15)

    def handle(self, *args, **params):
        room_name = params['name'].strip()[:10] # Trim the room name value to 10 characters
        seat_capacity = params['seat_capacity']

        with transaction.atomic():
            room_instance = Room(name=room_name)
            room_instance.save()

            seats = [Seat(room = room_instance) for i in range(0, seat_capacity)]
            Seat.objects.bulk_create(seats)

        print(f"Room '{room_name}' is successfully created with {seat_capacity} seats.")




