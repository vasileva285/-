from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Получить элемент из словаря по ключу"""
    if dictionary and isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def mul(value, arg):
    """Умножение значения на аргумент"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

