""" http://www.bitboost.com/ref/international-address-formats.html """
from django import forms
from django.utils.translation import ugettext_lazy as _
from localflavor.au.forms import AUPostCodeField, AUStateSelect

from postal.forms import PostalAddressForm

class AUPostalAddressForm(PostalAddressForm):
    line1 = forms.CharField(label=_(u"Street"), max_length=50)
    line2 = forms.CharField(label=_(u"Area"), required=False, max_length=100)
    city = forms.CharField(label=_(u"City"), max_length=50)
    state = forms.CharField(label=_(u"US State"), widget=AUStateSelect)
    code = AUPostCodeField(label=_(u"Zip Code"))

    def __init__(self, *args, **kwargs):
        super(AUPostalAddressForm, self).__init__(*args, **kwargs)
        self.fields['country'].initial = "AU"
