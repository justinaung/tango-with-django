from django import template
from apps.rango.models import Category

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(category=None):
    return {
        'categories': Category.objects.all(),
        'act_cat': category
    }
