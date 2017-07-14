from django.conf.urls import url
from .views import RegistrationView, LoginView

urlpatterns = [
    url(r'^register', RegistrationView.as_view(), name='register'),
    url(r'^login', LoginView.as_view(), name='login'),
]
