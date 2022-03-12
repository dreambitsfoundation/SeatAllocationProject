from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError, NotFound

from api.models import Room, SeatAllocation
from api.serializers import StudentSerializer, ClassroomSerializer
from api.views import get_list_of_class_rooms_with_x_students

class ClassroomsWithXStudents(APIView):
    """
    Get the class room with atleast X seat allocation.
    """

    def get(self, request, format=None):
        min_student_count = request.GET.get("count", 15)
        rooms_with_min_x_students = get_list_of_class_rooms_with_x_students(min_student_count)
        room_ids = [room['room_id'] for room in rooms_with_min_x_students]
        room_instances = Room.objects.filter(pk__in=room_ids)
        serializer = ClassroomSerializer(room_instances, many=True)
        return Response(serializer.data)
