from django.urls import path, include
from .views import HomeView, PostList, ReplyList

urlpatterns = [
    path('home/', HomeView.as_view(), name="Home"),
    path('posts/', include('app.urls_list.urls_post')),
    path('myreplies/', include('app.urls_list.urls_reply'))
]