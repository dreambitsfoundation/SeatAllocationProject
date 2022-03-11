from api.serializers import ClassroomSerializer
from api.models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Classroom(APIView):
    #serializer_class = ClassroomSerializer

    def get(self, request):
        queryset = Room.objects.all()
        serializer = ClassroomSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
