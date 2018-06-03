from django import template

from app.main.models import Type, CourseDiscipline

register = template.Library()


@register.inclusion_tag('inc/filter.html', takes_context=True)
def type_choice(context):
    current_type = context['request'].GET.get('typeFilter', -1)
    current_block = context['request'].GET.get('blockFilter', -1)
    return {
        'type_choices': Type.objects.all(),
        'current': int(current_type) if current_type else None,
        'block_choices': CourseDiscipline.objects.filter(course=context['course']) if context['course'] else None,
        'current_block': int(current_block) if current_block else None
    }
