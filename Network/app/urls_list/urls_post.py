from django.urls import path
from app.views import PostDetail, PostList, PostCreate, PostDetail, PostUpdate, ReplyCreate, MyPostList

urlpatterns = [
    path('', PostList.as_view(), name="Posts"),
    path('create/', PostCreate.as_view(), name="Posts_create"),
    path('<int:pk>/', PostDetail.as_view(), name="Posts_detail"),
    path('<int:pk>/update/', PostUpdate.as_view(), name="Posts_update"),
    path('myposts/', MyPostList.as_view(), name="MyPosts"),
    #Create reply
    path('<int:pk>/reply/', ReplyCreate.as_view(), name="Reply_create"),
]