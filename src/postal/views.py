from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
try:
    from django.utils import simplejson
except ImportError:
    import json as simplejson
from postal.library import form_factory
from postal.settings import POSTAL_USE_CRISPY_FORMS


def address_inline(request, prefix="", country_code=None, template_name="postal/form.html"):
    """ Displays postal address with localized fields """
    country_prefix = "country"
    prefix = request.POST.get('prefix', prefix)

    if prefix:
        country_prefix = prefix + '-country'
    country_code = request.POST.get(country_prefix, country_code)
    postal_form_id = request.POST.get('postal-form-id', 'postal-address-form')

    form_class = form_factory(country_code=country_code)

    if request.method == "POST":
        data = {}
        for (key, val) in request.POST.items():
            if val is not None and len(val) > 0:
                data[key] = val
        data.update({country_prefix: country_code})

        form = form_class(prefix=prefix, initial=data, postal_form_id=postal_form_id)
    else:
        form = form_class(prefix=prefix, postal_form_id=postal_form_id)

    return render_to_string(
        template_name,
        context={
            "form": form,
            "prefix": prefix,
        },
        request=request
    )


def changed_country(request):
    if POSTAL_USE_CRISPY_FORMS:
        result = simplejson.dumps({
            "postal_address": address_inline(request, template_name="postal/crispyform.html")
        })
    else:
        result = simplejson.dumps({
            "postal_address": address_inline(request),
        })
    return HttpResponse(result)