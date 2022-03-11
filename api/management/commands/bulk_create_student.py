from django.core.management.base import BaseCommand, CommandParser
from api.models import Room, Seat, Student, StudentBatch
from django.db import transaction

class Command(BaseCommand):
    help = "Create students in bulk in batches."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('count', type=int, help="Number of new students to be created", default=0)

    def handle(self, *args, **params):
        record_count = params['count']

        if not record_count:
            raise RuntimeError("Please provide the number of records to be created.")

        try:
            with transaction.atomic():
                new_batch_instance = StudentBatch.objects.create()
                new_batch_instance.save()

                new_students = [self.create_student_instance(new_batch_instance.pk, i) for i in range(0, record_count)]
            
                new_batch_instance.students.add(*new_students)
                new_batch_instance.save()
                
                print(f"{record_count} student(s) were created in batch {new_batch_instance.pk}")
        except Exception as e:
            print("There was an issue with the batch execution.")
            raise e

    def create_student_instance(self, batch_id: int, index: int):
        student = Student(name=f"STUDENT_B{batch_id}_S{index}", email_id=f"student.b{batch_id}.s{index}@school.com")
        student.save()
        return student





