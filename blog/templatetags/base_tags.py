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

@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, content, classes):
    return {
        "request": request,
        "link_name": link_name,
        "link": "account:{}".format(link_name),
        "content": content,
        "classes": classes,
    }