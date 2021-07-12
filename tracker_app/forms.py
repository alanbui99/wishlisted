from django import forms
from .models import Item
from urllib.parse import urlsplit


class ItemForm(forms.Form):
    def __init__(self, email='', *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

        self.fields['url'] = forms.URLField(label='Amazon URL', widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.amazon.com/...'
        }))

        self.fields['email'] = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'value': email
        }))

        self.fields['notify_when'] = forms.CharField(label='Notify when price', widget=forms.RadioSelect(choices=[
            ('below', 'is below a certain price'),
            ('down', 'goes down'),
            ('change', 'changes'),
            ('no', 'do not notify')
        ],  attrs={
            'class': 'list-unstyled',
            'onchange': 'displayDesiredPrice();'
        }),
            initial='below')

        self.fields['desired_price'] = forms.DecimalField(decimal_places=2, required=False, widget=forms.NumberInput(attrs={
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
        domain, path = urlsplit(url)[1:3]
        if domain != 'www.amazon.com':
            raise forms.ValidationError("URL Must be from www.amazon.com")
        path = path.split('ref')[0]
        sanitized_url = 'https://' + domain + path
        return sanitized_url


class EmailForm(forms.Form):
    def __init__(self, value='', *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(widget=forms.EmailInput(attrs={
            'placeholder': 'Enter Your Email Address',
            'value': value
        }))
