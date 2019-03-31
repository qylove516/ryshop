from django.urls import path
from users import views
urlpatterns = [
    path(r'jwt/', views.JWTAPIView.as_view(), name='jwt'),

]
