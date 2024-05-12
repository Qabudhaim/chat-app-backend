from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('get-token/', views.TokenView.as_view(), name='get-token'),
    path('whoami/', views.WhoAmI.as_view(), name='whoami'),
    path('api/list-users/', views.ListUsersView.as_view(), name='list-users'),
    path('api/filter-users/', views.FilterUsersView.as_view(), name='filter-users'),
    path('api/list-rooms/', views.ListRoomsView.as_view(), name='list-rooms'),
    path('api/create-room/', views.CreateRoomView.as_view(), name='create-room'),
    path('api/messages/', views.GetMessagesView.as_view(), name='get-messages'),
    path('api/send-message/', views.SendMessageView.as_view(), name='send-message'),
    path('api/last-messages/', views.LastMessagesView.as_view(), name='last-message'),
    path('api/list-rooms-and-messages/',
         views.ListRoomsAndLastMessagesView.as_view(), name='list-rooms-and-messages'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('chat/<str:room_name>/', views.room, name='room'),

]
