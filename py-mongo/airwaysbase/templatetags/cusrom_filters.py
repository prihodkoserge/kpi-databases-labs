from django import template

register = template.Library()


@register.filter(name='add_css_class')
def add_css_class(value, classname):
    return value.as_widget(attrs={'class': classname})

@register.filter(name="private_attr")
def private_attr(dic, key):
    return dic[key]