from wsgiref.handlers import format_date_time
from django.core.management.base import BaseCommand, CommandParser
from api.models import Room, Seat, SeatAllocation
from django.db import transaction
import datetime
from django.db.models import Q

from api.views import get_student

class Command(BaseCommand):
    help = "This command is used to create new room with a number as seats."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('student_id', type=int, help="ID of the student we're querying for")
        parser.add_argument('--date', type=str, help="Date of query DD-MM-YYYY")

    def handle(self, *args, **params):
        student_id = params['student_id']
        print(params['date'])
        try:
            query_date = datetime.datetime.strptime(params['date'], '%Y-%m-%d')
            print(query_date.day)
            print(query_date.month)
            print(query_date.year)
        except Exception as e:
            print("Could not parse the date.")
            return

        results = SeatAllocation.objects.filter(date_of_allocation__gte=query_date, student__pk=student_id).order_by('date_of_allocation')
        print(results)
        if results.count():
            result = results[0]
            print(f"Student {result.student.name} was allocated seat {result.seat.id} at {result.seat.room.name} room on {params['date']}")
        else:
            print(f"This student was not allocated any seat on {params['date']}")
