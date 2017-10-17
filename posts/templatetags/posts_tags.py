from django import template
from posts.models import PostCategory

register = template.Library()

@register.inclusion_tag('posts/tags/categories.html', takes_context=True)
def categories(context):
    return {
        'categories': PostCategory.objects.all(),
        'request': context['request'],
    }