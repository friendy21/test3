from django.urls import path
from .views.views import UserCreateView

urlpatterns = [
    path('<uuid:org_id>/users/', UserCreateView.as_view(), name='create-user'),
]