from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import views

from .serializer import InviteUserSerializer
from .tasks import send_verification_code


class InviteUserView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InviteUserSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            send_verification_code(instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


