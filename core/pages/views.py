from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'pages/home.html'
    

class TestPageView(TemplateView):
    template_name = 'pages/test.html'

