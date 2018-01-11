from django import template
import re

wikilink = re.compile("\[\[([^\]]+)\]\]")
wikiurl = re.compile("\[([^|]+)|([^\]]+)\]")
register = template.Library()

@register.filter
def wikify(value):
    text = wikilink.sub(r"<a href='/wiki/hanchi/\1/'>\1</a>", value)
    return wikiurl.sub(r"<a href='\2'>\1</a>", text)
