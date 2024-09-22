from django import template

register = template.Library()

@register.filter(name='repeat')
def repeat(value, times):
    """指定した回数だけ文字列を繰り返すフィルタ"""
    return value * int(times)