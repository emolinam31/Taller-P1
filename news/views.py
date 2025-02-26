from django.shortcuts import render
from .models import News

def news(request):
    news = News.objects.all().order_by("-date")  # -date es para ordenar por date de mas recientes a menos (-)
    return render(request, "news.html", {"news": news})

