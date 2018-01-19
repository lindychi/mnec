from django import template
import re

wikilink = re.compile("\[\[([^\]]+)\]\]")
wikiurl = re.compile("\[([^|]+)\|([^\]]+)\]")
register = template.Library()


@register.filter
def wikify(value):
    """Substitute the wiki syntax."""
    value = wikiurl.sub(r"<a href='\2'>\1</a>", value)
    return wikilink.sub(r"<a href='/wiki/hanchi/\1/'>\1</a>", value)
