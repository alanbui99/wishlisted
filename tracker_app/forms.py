from django import forms
from .models import Item
from urllib.parse import urlparse

# class ItemForm(forms.ModelForm):
#     class Meta:

#         model = Item
#         fields = ('url', 'email', 'notify_when', 'desired_price')
#         labels = {
#             'url': ('Amazon URL'),
#             'notify_when': ('Notify when price'),
#             'desired_price': ('Notify when price is below')
#         }
#         widgets = {
#             'url': forms.URLInput(attrs={'class': 'form-control mb-4', 'placeholder':'https://www.amazon.com/...'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control mb-4'}),
#             'notify_when': forms.RadioSelect(choices=NOTIFY_CHOICES, attrs={'class': 'list-unstyled mx-3', 'onchange': "configDisplay();"}),
#             'desired_price': forms.NumberInput(attrs={'class': 'form-control'}),
#         }

class ItemForm(forms.Form):
    NOTIFY_CHOICES = [
        ('below', 'is below a certain price'),
        ('down', 'goes down'),
        ('change', 'changes'),
    ]

    url = forms.URLField(label='Amazon URL', widget=forms.URLInput(attrs= {
        'class': 'form-control mb-4',
        'placeholder': 'https://www.amazon.com/...'
    }))

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs= {
        'class': 'form-control mb-4'
    }))

    notify_when = forms.CharField(widget=forms.RadioSelect(choices=NOTIFY_CHOICES,  attrs= {
        'class': 'list-unstyled', 
        'onchange': 'displayDesiredPrice();'
    }), 
    initial='below')

    desired_price = forms.DecimalField(decimal_places=2, required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Notify when price is below',
        'min': 0
    }))

    def clean_desired_price(self):
        price = self.cleaned_data.get('desired_price')
        if price and price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        price = float(price) if price else price
        return price

    def clean_url(self):
        url = self.cleaned_data.get('url')
        domain = urlparse(url)[1]
        if domain != 'www.amazon.com':
            raise forms.ValidationError("URL Must be from www.amazon.com")
        return url
        


