from django import template
import re

wikilink = re.compile("\[\[([^\]]+)\]\]")
register = template.Library()

@register.filter
def wikify(value):
    return wikilink.sub(r"<a href='/wiki/hanchi/\1/'>\1</a>", value)
