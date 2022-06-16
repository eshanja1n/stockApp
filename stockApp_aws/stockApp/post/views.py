from tracemalloc import start
from django.shortcuts import render, redirect
from django.http import HttpResponse

from post.models import Post
from post.forms import CreatePostForm
from account.models import Account

import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datetime import datetime
from datetime import timedelta

import uuid
from django.views.decorators.clickjacking import xframe_options_sameorigin

import os


# Create your views here.


def create_post(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('home')
    

    if request.POST:
        form = CreatePostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            author = Account.objects.filter(username=user.username).first()
            
            buyDateBeg = datetime.strptime(obj.buyDate, "%Y-%m-%d")
            sellDateBeg = datetime.strptime(obj.sellDate, "%Y-%m-%d")
            endDate = sellDateBeg + timedelta(days=1)
            sellDate = str(endDate)
            adjSellDate = sellDate[:10]

            tick = yf.Ticker(obj.ticker)
            hist = tick.history(start=obj.buyDate, end=adjSellDate, interval="1d")

            # fig = go.Figure(data=go.Scatter(x=hist.index,y=hist['Close'], mode='lines'))
            fig3 = make_subplots(specs=[[{"secondary_y": True}]])
            fig3.add_trace(go.Candlestick(x=hist.index,
                                        open=hist['Open'],
                                        high=hist['High'],
                                        low=hist['Low'],
                                        close=hist['Close'],
                                        ))
            fig3.update_layout(xaxis_rangeslider_visible=False)
            fig3.update_xaxes(rangebreaks = [
                       dict(bounds=['sat','mon']), # hide weekends
                       #dict(bounds=[16, 9.5], pattern='hour'), # for hourly chart, hide non-trading hours (24hr format)
                       dict(values=["2021-12-25","2022-01-01"]) #hide Xmas and New Year
            ])
            
            hex = str(uuid.uuid4().hex)
            path = f'graphs/{str(hex)}.html'
            fig3.write_html(path)

            openPrice = hist["Open"][obj.buyDate]
            closePrice = hist["Close"][obj.sellDate]

            percentChange = ((float(closePrice) - float(openPrice)) / float(openPrice)) * float(100)
            
            obj.percentChange = percentChange
            obj.author = author
            obj.hex = hex
            obj.graph = path

            buy = buyDateBeg.strftime("%b %d, %Y")
            month, day, year = buy.split()
            if day[0] == '0':
                day = day[1] + ", "
            buyDate = month + " " + day  + year

            sell = sellDateBeg.strftime("%b %d, %Y")
            month, day, year = sell.split()
            if day[0] == '0':
                day = day[1] + ', '
            sellDate = month + " " + day + year



            obj.buyDate = buyDate
            obj.sellDate = sellDate

            obj.save()
            return redirect('home')
        else:   
            context['form'] = form
    else:
        form = CreatePostForm()
        context['form'] = form
    
    return render(request, 'post/create_post.html', context)

@xframe_options_sameorigin
def show_graph(request, hex):
    path = f'graphs/{str(hex)}.html'
    content = open(path)
    return HttpResponse(content)




def delete_post_view(request, id):
    post = Post.objects.get(id=id)
    os.remove(post.graph)
    post.delete()
    # print(post.graph)
    return redirect('profile', request.user.username)