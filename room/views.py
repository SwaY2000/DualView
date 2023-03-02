from rest_framework import status, views
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Video
from .permissions import IsStuffAndAuthenticated
from .serializers import VideoSerializer


class VideoView(views.APIView):
    permission_classes = [IsStuffAndAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        serializer = VideoSerializer(get_object_or_404(
            Video, id=pk
        ), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        serializer = VideoSerializer(
            get_object_or_404(
                Video,
                id=id
            )
        )
        return Response(serializer.data)

    def put(self, request, id, format=None):
        serializer = VideoSerializer(
            get_object_or_404(
                Video,
                id=id
            ),
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
