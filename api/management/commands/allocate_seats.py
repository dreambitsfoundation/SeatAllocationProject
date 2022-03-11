from django.core.management.base import BaseCommand, CommandParser
from api.models import Room, Seat, SeatAllocation, Student, StudentBatch
from django.db import transaction

class Command(BaseCommand):
    help = "Create students in bulk in batches."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('batch_id', type=int, help="Batch Id of the students to be allocated.", default=0)
        parser.add_argument('room_name', type=str, help="Name of the room to be allocated to the batch of students", default=0)


    def handle(self, *args, **params):
        batch_id = params['batch_id']
        room_name = params['room_name']

        batch_instances = StudentBatch.objects.filter(pk=batch_id)
        if not batch_instances.count():
            raise RuntimeError(f"Batch ID {batch_id} was not found in the records.")

        room_instances = Room.objects.filter(name = room_name)
        if not room_instances.count():
            raise RuntimeError(f"Room: {room_name} was not found in the records.")

        batch_size = batch_instances[0].students.all().count()
        total_seat_allocation = Seat.objects.filter(room=room_instances[0])
        
        if total_seat_allocation.count() < batch_size:
            raise RuntimeError("Seat capacity of the room is less then the batch size")
        
        allocated_seat_capacity_of_the_room = SeatAllocation.objects.filter(seat__room=room_instances[0], date_of_withhold__isnull=True).count()

        current_seat_capacity = total_seat_allocation.count() - allocated_seat_capacity_of_the_room

        if current_seat_capacity < batch_size:
            raise RuntimeError("Available Seat capacity is less then the batch size.")

        # Allocate seats to each student
        available_seats = list(Seat.objects.filter(room=room_instances[0], allocated=False))[:batch_size]

        students = list(batch_instances[0].students.all())

        seat_allocations = [SeatAllocation(seat=seat, student=student) for seat, student in zip(available_seats, students)]

        for seat_allocation in seat_allocations:
            seat_allocation.save()

        print(f"Seat allocation is successfully completed for batch ID {batch_id} into {room_instances[0].name} for {batch_size} students.")