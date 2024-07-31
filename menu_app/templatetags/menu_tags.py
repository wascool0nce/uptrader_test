from django import template
from menu_app.models import Menu, MenuItem
from django.urls import resolve

register = template.Library()


def is_active_item(item, current_url):
    if item.url == current_url or item.named_url and resolve(current_url).url_name == item.named_url:
        return True
    for child in item.children.all():
        if is_active_item(child, current_url):
            return True
    return False


@register.inclusion_tag('menu_app/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    menu = Menu.objects.prefetch_related('items__children').get(name=menu_name)
    items = menu.items.filter(parent=None)
    active_items = [item for item in items if is_active_item(item, current_url)]
    return {
        'items': items,
        'current_url': current_url,
        'active_items': active_items,
    }
