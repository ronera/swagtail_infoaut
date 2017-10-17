from django import template
from posts.models import PostCategory, PostPage

register = template.Library()

@register.inclusion_tag('posts/tags/categories.html', takes_context=True)
def categories(context):
    return {
        'categories': PostCategory.objects.all(),
        'request': context['request'],
    }

@register.inclusion_tag('posts/tags/events.html', takes_context=True)
def events(context):
    events_posts = PostPage.objects.live().order_by(
        '-first_published_at',
    ).filter(
        categorie__name="Agenda",
    )
    return {
        'events_posts': events_posts,
        'request': context['request'],
    }
