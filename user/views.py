from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import views, status

from .serializer import InviteUserSerializer, ActivateUserSerializer, UserSerializer
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

    def put(self, request):
        if email := request.data.get('email'):
            send_verification_code(
                get_object_or_404(
                    get_user_model(),
                    email=email,
                    is_active=False,
                )
            )
            Response('Resend verification_code is successful.', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)


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


class UserFriend(views.APIView):
    def post(self, request):
        friend = get_object_or_404(get_user_model(), id=request.data.get('id', ''))
        if request.user == friend:
            return Response({'error': 'You cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.send_friend_request(friend)
        return Response({'success': 'Friend request sent'}, status=status.HTTP_200_OK)

    def put(self, request):
        friend = get_object_or_404(get_user_model(), id=request.data.get('id', ''))
        if friend not in request.user.friend_requests_received.all():
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
        request.user.accept_friend_request(friend)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        friend = get_object_or_404(get_user_model(), id=request.data.get('id', ''))

        if friend not in request.user.friend_requests_received.all() and friend not in request.user.friend.all():
            return Response({'error': 'User is not your friend'}, status=status.HTTP_404_NOT_FOUND)

        if friend in request.user.friend_requests_received.all():
            request.user.reject_friend_request(friend)
        else:
            request.user.unfriend(friend)

        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
