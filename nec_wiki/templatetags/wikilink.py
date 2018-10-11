from django import template
import re

wikiotherlink = re.compile("\[\[([^\|]+)\|([^\]]+)\]\]")
youtubelink = re.compile(r"youtube=([0-9a-zA-Z]+)")
register = template.Library()


@register.filter
def wikify(value):
    """Substitute the wiki syntax."""
    value = wikiotherlink.sub(r"<a href='/wiki/page/\2'>\1</a>", value)
    value = youtubelink.sub(r'<iframe width="560" height="315" src="https://www.youtube.com/embed/\1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', value)
    return value
