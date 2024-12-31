import json
import os
import re

from django import template


from django.conf import settings
from website.models import CustomSetting, TranslateNavbar, FormPage, LocationMarker
from website.serializers import LocationMarkerSerializer

register = template.Library()


@register.simple_tag(takes_context=True)
def get_navbartrans(context) -> "QuerySet[Navbar]":
    layout: CustomSetting = CustomSetting.for_request(context["request"])
    navbarorderables = layout.site_navbartrans.all()
    language_code = context.request.LANGUAGE_CODE
    navbars = TranslateNavbar.objects.filter(
        transnavbarorderable__in=navbarorderables
    ).order_by("transnavbarorderable__sort_order")
    trans_keys = [item.translation_key for item in navbars]
    results = TranslateNavbar.objects.filter(
        translation_key__in=trans_keys, locale__language_code=language_code
    )
    return results


@register.simple_tag(takes_context=True)
def get_contact_form(context) -> "QuerySet[Navbar]":
    form_page = FormPage.objects.first()
    result = form_page.get_form(context["request"])
    return result


@register.simple_tag
def get_location_marker():
    loc = LocationMarker.objects.all()
    serializer = LocationMarkerSerializer(loc, many=True).data
    json_data = json.dumps(serializer)
    return json_data


@register.filter
def original_url(image):
    return os.path.join(settings.MEDIA_URL, str(image.file))


@register.filter
def hide_num_order(title):
    number_match = re.match(r'^.*?\[[^\d]*(\d+)[^\d]*\].*$', title)
    if number_match:
        number = number_match.group(1)
        return title.replace('[{}]'.format(number), '')
    return title
