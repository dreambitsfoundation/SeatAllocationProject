from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from api.serializers import StudentSerializer
from api.views import change_classroom_allocation

class ChangeRoomAllocation(APIView):
    """
    Takes a POST request with the student Id and the target classroom ID and returns all the 
    allocations in the new classroom.
    """

    def post(self, request, format=None):
        payload = request.data
        student_id = payload.get("student_id", None)
        classroom_id = payload.get("classroom_id", None)
        if not student_id or not classroom_id:
            raise APIException("Classroom ID or Student ID was not provided.")
        students_in_the_new_class = change_classroom_allocation(student_id, classroom_id)
        serializer = StudentSerializer(students_in_the_new_class, many=True)
        return Response(serializer.data)
