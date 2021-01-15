from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from urllib.parse import urlencode

from .models import Item
from .forms import ItemForm
from .scraper import scrape

# Create your views here.
def home(request):
    return render(request, 'tracker_app/home.html')

def register(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        # try:
        email_input = form.cleaned_data.get('email')
        if User.objects.filter(username=email_input).exists():
            user = User.objects.filter(username=email_input).first()
        else:
            user = User.objects.create_user(email_input)
        
        new_item = Item.objects.create(
            url=form.cleaned_data.get('url'),
            notify_when=form.cleaned_data.get('notify_when'),
            desired_price=form.cleaned_data.get('desired_price'),
            user=user
        )

        payload = scrape(new_item, init=True)
        new_item.init_price = payload.get('current_price')
        new_item.landing_image = payload.get('landing_image')
        new_item.save()
        new_item.record_set.create(price=payload.get('current_price'), emailed=payload.get('emailed'))

        notify_choices_mapper = {
            'below': 'is below ',
            'down': 'goes down',
            'change': 'changes',
            'no': 'no'
        }
        
        new_item.notify_when = notify_choices_mapper[new_item.notify_when]

        return render(request, 'tracker_app/confirm.html', {'details': payload, 'item': new_item})

        # except Exception as e: 
        #     print(str(e))


    return render(request, 'tracker_app/register.html', {'form': form, 'processing': False})
