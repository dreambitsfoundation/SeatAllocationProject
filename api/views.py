from tkinter import E
from django.db.models import Count, F
from django.db import transaction
from django.utils import timezone
from api.models import Room, Student, StudentBatch, Seat, SeatAllocation

from rest_framework.exceptions import APIException, ParseError, NotFound

def get_student(student_id: int):
    try:
        return Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise APIException("Student was not found in the database.")

def get_classroom(classroom_id: int):
    try:
        return Room.objects.get(pk=classroom_id)
    except Room.DoesNotExist:
        raise APIException("Classroom was not found in the database")

def get_list_of_students_seated_in_a_given_classroom(class_room_id: int):
    """ 
    Returns the list of students to a given classroom id
    """
    class_room_instance = get_classroom(class_room_id)
    students_list = [allocation.student for allocation in SeatAllocation.objects.filter(seat__room=class_room_instance, date_of_withhold__isnull=True)]

    return students_list


def get_list_of_class_rooms_with_x_students(student_count: int = 0, return_only_max: bool = False):
    """ 
    Takes student count as an argument and returns
    
    1. All the rooms with active StudentAllocation instance count >= student_count (if return_only_max = False)
    2. Only the room with max active StudentAllocation instance (if return_only_max = True)
    
    """
    if student_count == 0 and not return_only_max:
        return [{'room_id': r.id} for r in Room.objects.all()]
    
    rooms = SeatAllocation.objects.filter(date_of_withhold__isnull=True)\
        .values('seat__room')\
        .annotate(count=Count('pk', disctinct=True))\
        .order_by('-count')

    if not return_only_max:
        rooms = rooms.filter(count__gte=student_count)
    
    rooms = rooms.annotate(room_id=F('seat__room'))\
            .values('room_id')

    return list(rooms if not return_only_max else rooms[:1])


def which_seat_student_is_allocated(student: Student):
    try:
        existing_room_allocation: SeatAllocation = SeatAllocation.objects.get(student=student, date_of_withhold__isnull=True)
        return existing_room_allocation
    except:
        return None

def withdraw_seat_allocation(seat_allocation: SeatAllocation):
    seat_allocation.date_of_withhold = timezone.now()
    seat_allocation.seat.allocated = False
    seat_allocation.save()

    print(seat_allocation.date_of_withhold)

def get_empty_seats_in_the_classroom(classroom: Room):
    return Seat.objects.filter(room=classroom, allocated=False)

def allocate_new_seat(student: Student, seat: Seat):
    allocation_instance = SeatAllocation(student=student, seat=seat)
    allocation_instance.save()

def initiate_seat_allocation(student: Student, current_seat: SeatAllocation, new_classroom: Room):
    try:
        with transaction.atomic():
            # Withdraw the current seat.
            withdraw_seat_allocation(current_seat)
            print("Seat Withdrawl complete")
            # Get all the empty seats in the new classroom
            empty_seats = get_empty_seats_in_the_classroom(new_classroom)
            if not len(empty_seats):
                raise APIException("There is not empty seats in this classroom")
            # Create a New Seat Allocation Record.
            target_seat = empty_seats[0]
            allocate_new_seat(student, target_seat)
    except Exception as e:
        raise e



def change_classroom_allocation(student_id, target_classroom_id):
    student = get_student(student_id)
    new_classroom = get_classroom(target_classroom_id)

    current_seat = which_seat_student_is_allocated(student)
    if current_seat and current_seat.seat.room != new_classroom:
        initiate_seat_allocation(student, current_seat, new_classroom)

    return get_list_of_students_seated_in_a_given_classroom(new_classroom.id)
