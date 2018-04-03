from django import template
import re

wikilink = re.compile("\[\[([^\]|]+)\]\]")
wikiurl = re.compile("\[([^|]+)\|([^\]]+)\]")
register = template.Library()


@register.filter
def wikify(value):
    """Substitute the wiki syntax."""
    newline_value = re.sub(r"\n", "<br />", value)
    wikilink_value = wikilink.sub(r"<a href='/wiki/page/\1/'>\1</a>", newline_value)
    wikiurl_value = wikiurl.sub(r"<a href='\2'>\1</a>", wikilink_value)
    return wikiurl_value
