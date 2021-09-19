from django_filters import FilterSet
from .models import Reply

class PostFilter(FilterSet):
    class Meta:
        model = Reply
        fields = {
            'post__title': ['icontains',],
        }