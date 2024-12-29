from django import template
from .. models import Settings, Category

register = template.Library()

@register.simple_tag
def title():
    return Settings.objects.all()[0]

@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        'categories': Category.objects.filter(status=True)
    }