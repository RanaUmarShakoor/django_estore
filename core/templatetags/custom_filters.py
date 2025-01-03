from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def update_query_param(context, param_name, param_value):
    # Get the current request and its query parameters
    query = context['request'].GET.copy()

    # Update the parameter or add it if it doesn't exist
    if param_value:
        query[param_name] = param_value
    else:
        query.pop(param_name, None)  # Remove parameter if no value is passed

    # Rebuild the query string with the updated parameters
    return '?' + urlencode(query)


@register.filter
def mul(value, arg):
    return value * arg
