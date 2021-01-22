from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from urllib.parse import urlencode

from .models import Item
from .forms import ItemForm

# Create your views here.
def home(request):
    return render(request, 'tracker_app/home.html')

def register(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        new_item_id = Item.register(form.cleaned_data)
        if not new_item_id: return redirect('tracking-error')
        request.session['item_id'] = str(new_item_id)
        return redirect('confirm')

    return render(request, 'tracker_app/register.html', {'form': form, 'processing': False})

def confirm(request):
    item_id = request.session.get('item_id')
    item = Item.objects.filter(id=item_id).first()
    print(item)
    return render(request, 'tracker_app/confirm.html', {'item': item})

def tracking_error(request):
    return render(request, 'tracker_app/tracking-error.html')

