from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .Views import students_in_a_class_room_view, rooms_with_x_students, change_room_allocation, rooms

urlpatterns = [
    path('studentsInClassroom/<int:classroom_id>', students_in_a_class_room_view.StudentInAClassRoomView.as_view()),
    path('classroomsWithXStudents', rooms_with_x_students.ClassroomsWithXStudents.as_view()),
    path('changeClassroom', change_room_allocation.ChangeRoomAllocation.as_view()),
    path('classroom', rooms.Classroom.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)