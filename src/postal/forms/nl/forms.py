from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from localflavor.nl.forms import NLZipCodeField

from postal.forms import PostalAddressForm

class MyNLZipCodeField(NLZipCodeField):
    def clean(self, value):
        if isinstance(value, six.string_types):
            value = value.upper().replace(' ', '')

        # don't strip the spaces out of the zipcode, it confuses
        # the geocoders
        return super(NLZipCodeField, self).clean(value)
 

class NLPostalAddressForm(PostalAddressForm):    
    line1 = forms.CharField(label=_(u"Street"), max_length=100)
    line2 = forms.CharField(label=_(u"Area"), required=False, max_length=100)
    city = forms.CharField(label=_(u"Town/City"), max_length=100)
    code = MyNLZipCodeField(label=_(u"Zip Code"))
    
    
    class Meta:
        exclude = ('state',)
    
    def __init__(self, *args, **kwargs):
        super(NLPostalAddressForm, self).__init__(*args, **kwargs)
        # we have to manually pop the inherited line5
        self.fields.pop('state')
        self.fields['country'].initial = "NL"
