from django import template
from store.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'По цене',
            'sorters': [
                ('price', 'По возрастанию'),
                ('-price', 'По убыванию')
            ]
        }
    ]

    return sorters


@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)

