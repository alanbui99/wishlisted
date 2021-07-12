from urllib.parse import urlencode
from json import dumps

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Item
from .models import Record
from .forms import ItemForm
from .forms import EmailForm

def home(request):
    return render(request, 'tracker_app/home.html')

def register(request):
    form = ItemForm(email=request.session.get('email') or '')
    if form.is_valid():
        new_item_id = Item.register(form.cleaned_data)
        if not new_item_id:
            return redirect('tracking-error')

        # save data in session
        request.session['item_id'] = str(new_item_id)
        request.session['email'] = form.cleaned_data.get('email')
        return redirect('confirm')

    return render(request, 'tracker_app/register.html', {'form': form, 'processing': False})


def confirm(request):
    item_id = request.session.get('item_id')
    if not item_id:
        return redirect('/')
    item = Item.objects.filter(id=item_id).first()
    return render(request, 'tracker_app/confirm.html', {'item': item})


def unsubscribe(request, item_id):
    item = Item.unsubscribe(item_id)
    if not item:
        return render(request, 'tracker_app/unsubscribe-failed.html')
    return render(request, 'tracker_app/unsubscribe-succeeded.html', {'item': item})


def item_list(request):
    if(request.method == 'POST'):
        request.session['email'] = request.POST.get('email')

    email = request.session.get('email')
    if not email:
        return render(request, 'tracker_app/item-list.html', {'form': EmailForm(), 'email': None})

    items = Item.get_items_by_email(email)
    return render(request, 'tracker_app/item-list.html', {'form': EmailForm(value=email), 'items': items, 'email': email})

def item(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    dates, prices = Record.get_item_chart_data(item)
    return render(request, 'tracker_app/item-details.html', {'item': item, 'dates': dumps(dates), 'prices': dumps(prices)})

def tracking_error(request):
    return render(request, 'tracker_app/tracking-error.html')
