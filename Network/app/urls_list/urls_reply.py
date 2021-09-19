from django.urls import path
from app.views import ReplyList, ReplyDetail, ReplyDelete

urlpatterns = [
    path('', ReplyList.as_view(), name='Reply_list'),
    path('<int:pk>/', ReplyDetail.as_view(), name="Reply_detail"),
    path('<int:pk>/deny/', ReplyDelete.as_view(), name="Reply_delete")
]