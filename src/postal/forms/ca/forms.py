""" http://www.bitboost.com/ref/international-address-formats.html """
from django import forms
from django.utils.translation import ugettext_lazy as _
from localflavor.ca.forms import CAPostalCodeField, CAProvinceField, CAProvinceSelect

from postal.forms import PostalAddressForm


class CAPostalAddressForm(PostalAddressForm):
    line1 = forms.CharField(label=_(u"Street"), max_length=50)
    line2 = forms.CharField(label=_(u"Street (con\'t)"), required=False, max_length=100)
    city = forms.CharField(label=_(u"City"), max_length=50)
    state = CAProvinceField(label=_(u"Province"), widget=CAProvinceSelect)
    code = CAPostalCodeField(label=_(u"Postal Code"))

    def __init__(self, *args, **kwargs):
        super(CAPostalAddressForm, self).__init__(*args, **kwargs)
        self.fields['country'].initial = "CA"
