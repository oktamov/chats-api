from django.urls import path

from users.views import UserRegisterView, UserLoginView, UserProfileView, SendMessage, UserListView, UpdateMessageView, \
    UserMessageAuthorsList

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile/<str:username>', UserProfileView.as_view(), name='profile'),

    path('list', UserListView.as_view(), name='user-list'),
    path('chats/', UserMessageAuthorsList.as_view(), name='message-list'),
    path('chats/<int:pk>/send-message/', SendMessage.as_view(), name='send-message'),
    path('chats/messages/<int:message_id>/', UpdateMessageView.as_view(),
         name='update-message'),

]
