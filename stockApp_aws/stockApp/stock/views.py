from operator import attrgetter
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse

import yfinance as yf
import plotly.graph_objects as go

from post.models import Post
from account.models import Account

from operator import attrgetter
# Create your views here.


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")

    context = {}

    posts = sorted(Post.objects.all(), key=attrgetter('date_published'), reverse=True)
    context['posts'] = posts

    return render(request, 'stock/index.html', context)

def trial(request):
    return HttpResponse("Hello, world. You're at the trial index.")


def search_view(request):
    context = {}

    if request.method == "GET":
        context['type'] = "GET"         
        return render(request, 'stock/search.html', context)
    else:
        context["type"] = "POST"
        # print(request.POST)
        stock = request.POST.get('q')
        # print(stock)
        posts = sorted(Post.objects.filter(ticker=stock), key=attrgetter('date_published'), reverse=True)
        print(posts)
        context['posts'] = posts
        context['ticker'] = stock
        context['num_posts'] = len(posts)
        return render(request, 'stock/search.html', context)
    