from django.urls import path
from .views import HomePageView, TestPageView
app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('test/', TestPageView.as_view(), name='test'),

]
