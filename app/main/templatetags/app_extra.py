from django import template

from app.main.models import Type

register = template.Library()


@register.inclusion_tag('inc/filter.html', takes_context=True)
def type_choice(context):
    current = context['request'].GET.get('typeFilter', -1)
    return {
        'type_choices': Type.objects.all(),
        'current': int(current) if current else None
    }
