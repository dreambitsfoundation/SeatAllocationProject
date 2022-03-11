from django.db import models

class Student(models.Model):
    """ This model keeps record for each student """
    name = models.CharField(max_length=60, null=False)
    email_id = models.EmailField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentBatch(models.Model):
    """ This model is keeps record of all the students created in the batch"""
    students = models.ManyToManyField(Student)
    created_on = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    """ This model keeps record of all the individual rooms """
    name = models.CharField(max_length=10, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Seat(models.Model):
    """ This model keeps record of all the seats associated with each room """
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    allocated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SeatAllocation(models.Model):
    """ This model is used to keep record for seat allocation for a student in a room on a particular date range """
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True)
    date_of_allocation = models.DateField(auto_now_add=True)
    date_of_withhold = models.DateField(null=True)

    def save(self, *args, **kwargs) -> None:
        """ Before saving a record we're going to check if there is an existing active record associated with this seat allocation """
        if not self.date_of_allocation:
            existing_records = SeatAllocation.objects.filter(models.Q(seat=self.seat) | models.Q(student=self.student), date_of_withhold__isnull=True)
            print(existing_records)
            if existing_records.count():
                raise RuntimeError("This seat or student has active allocation.")
            else:
                self.seat.allocated = True
                self.seat.save()
        return super(SeatAllocation, self).save(*args, **kwargs)