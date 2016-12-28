from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries import data as country_data


from postal.settings import POSTAL_ADDRESS_LINE1, POSTAL_ADDRESS_LINE2, POSTAL_ADDRESS_CITY, POSTAL_ADDRESS_STATE, \
    POSTAL_ADDRESS_CODE, POSTAL_USE_CRISPY_FORMS

if POSTAL_USE_CRISPY_FORMS:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Layout, Div

country_list = sorted([('', '-'*45)] + list(country_data.COUNTRIES.items()))


class PostalAddressForm(forms.Form):
    line1 = forms.CharField(label=POSTAL_ADDRESS_LINE1[0], required=POSTAL_ADDRESS_LINE1[1], max_length=100)
    line2 = forms.CharField(label=POSTAL_ADDRESS_LINE2[0], required=POSTAL_ADDRESS_LINE2[1], max_length=100)
    city = forms.CharField(label=POSTAL_ADDRESS_CITY[0], required=POSTAL_ADDRESS_CITY[1], max_length=100)
    state = forms.CharField(label=POSTAL_ADDRESS_STATE[0], required=POSTAL_ADDRESS_STATE[1], max_length=100)
    code = forms.CharField(label=POSTAL_ADDRESS_CODE[0], required=POSTAL_ADDRESS_CODE[1], max_length=100)
    country = forms.ChoiceField(label=_(u"Country"), choices=country_list)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.state = ''
        if POSTAL_USE_CRISPY_FORMS:
            css_id = 'postal_address'
            if 'prefix' in kwargs:
                css_id = kwargs['prefix'] + '-' + css_id
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.layout = Layout(
                Div(
                    'line1',
                    'line2'
                    'city',
                    'country',
                    'state',
                    'code',
                    css_id=css_id,
                    css_class='postal_address'
                )
            )

    def clean_country(self):
        data = self.cleaned_data['country']
        if data not in country_data.COUNTRIES.keys():
            raise forms.ValidationError("You must select a country")
        return data
