from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries import data as country_data


from postal.settings import POSTAL_ADDRESS_LINE1, POSTAL_ADDRESS_LINE2, POSTAL_ADDRESS_CITY, POSTAL_ADDRESS_STATE, \
    POSTAL_ADDRESS_CODE, POSTAL_USE_CRISPY_FORMS

if POSTAL_USE_CRISPY_FORMS:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Layout, Div, Hidden


def country_sort_key(country_data):
    if country_data[0] == 'US':
        return 'AAA'
    if country_data[0] == 'CA':
        return 'AAAA'
    return country_data[1]


country_list = sorted([('', '-' * 45)] + list(country_data.COUNTRIES.items()), key=country_sort_key)

form_helpers = {}


def register_postal_form_helper(form_id, form_helper):
    form_helpers[form_id] = form_helper


class PostalAddressForm(forms.Form):
    line1 = forms.CharField(label=POSTAL_ADDRESS_LINE1[0], required=POSTAL_ADDRESS_LINE1[1], max_length=100)
    line2 = forms.CharField(label=POSTAL_ADDRESS_LINE2[0], required=POSTAL_ADDRESS_LINE2[1], max_length=100)
    city = forms.CharField(label=POSTAL_ADDRESS_CITY[0], required=POSTAL_ADDRESS_CITY[1], max_length=100)
    state = forms.CharField(label=POSTAL_ADDRESS_STATE[0], required=POSTAL_ADDRESS_STATE[1], max_length=100)
    code = forms.CharField(label=POSTAL_ADDRESS_CODE[0], required=POSTAL_ADDRESS_CODE[1], max_length=100)
    country = forms.ChoiceField(label=_(u"Country"), choices=country_list)

    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        postal_form_id = kwargs.pop('postal_form_id', 'postal-address-form')
        if POSTAL_USE_CRISPY_FORMS:
            css_id = 'postal_address'
            if prefix is not None:
                css_id = prefix + '-' + css_id
            if postal_form_id in form_helpers:
                self.helper = form_helpers[postal_form_id]
            else:
                self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.layout = Layout(
                Div(
                    'country',
                    'line1',
                    'line2',
                    'city',
                    'state',
                    'code',
                    css_id=css_id,
                    css_class='postal_address'
                ),
                Hidden('postal-form-id', postal_form_id),
            )
        super(PostalAddressForm, self).__init__(*args, **kwargs)

    def clean_country(self):
        data = self.cleaned_data['country']
        if data not in country_data.COUNTRIES.keys():
            raise forms.ValidationError("You must select a country")
        return data
