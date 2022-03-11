from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError, NotFound

from api.models import Room, SeatAllocation
from api.serializers import StudentSerializer
from api.views import get_list_of_students_seated_in_a_given_classroom


class StudentInAClassRoomView(APIView):
    """
    Get all the Students in a classroom.
    """

    def get(self, request, classroom_id, format=None):
        students_list = get_list_of_students_seated_in_a_given_classroom(class_room_id=classroom_id)
        serializer = StudentSerializer(students_list, many=True)
        return Response(serializer.data)
