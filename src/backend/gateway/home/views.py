from django.shortcuts import render
from django.views import View


# Create your views here.
# home view
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home/home.html")
