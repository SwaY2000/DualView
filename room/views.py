from rest_framework import status, views
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .serializers import VideoSerializer


class VideoView(views.APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
