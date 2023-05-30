from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserRegisterSerializers, UserLoginSerializer, UserProfileSerializers, MessageSerializer, \
    MessageUpdateSerializer
from .models import User, Message


# Create your views here.
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializers


class UserRegisterView(generics.CreateAPIView):
    queryset = User
    serializer_class = UserRegisterSerializers


class UserLoginView(generics.CreateAPIView):
    queryset = User
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, }, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializers
    lookup_field = 'username'


class SendMessage(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageUpdateSerializer

    def perform_create(self, serializer):
        sender = self.request.user
        recipient_id = self.kwargs['pk']
        recipient = User.objects.get(pk=recipient_id)
        serializer.save(sender=sender, recipient=recipient)


class UserMessageAuthorsList(generics.ListAPIView):
    serializer_class = UserProfileSerializers

    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(sent_messages__sender_id=user).distinct()


class UpdateMessageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        message_id = self.kwargs['message_id']
        return Message.objects.get(id=message_id, sender=user)
