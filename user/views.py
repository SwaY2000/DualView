from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import views, status

from .serializer import InviteUserSerializer, ActivateUserSerializer
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


class ActivateUserView(views.APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        if email := request.data.get('email'):
            serializer = ActivateUserSerializer(
                data=request.data,
                instance=get_object_or_404(
                    get_user_model(),
                    email=email,
                    is_active=False,
                )
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

