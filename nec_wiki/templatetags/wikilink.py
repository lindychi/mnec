from django import template
import re

wikilink = re.compile("\[\[([^\|]]+)\]\]")
wikiotherlink = re.compile("\[\[([^|]+)|([^\]]+)\]\]")
wikiurl = re.compile("\[([^|]+)\|([^\]]+)\]")
youtubelink = re.compile(r"youtube=([0-9a-zA-Z]+)")
register = template.Library()


@register.filter
def wikify(value):
    """Substitute the wiki syntax."""
    wikiotherlink_value = wikiotherlink.sub(r"<a href='/wiki/page/\2'>\1</a>", value)
    wikilink_value = wikilink.sub(r"<a href='/wiki/page/\1'>\1</a>", wikiotherlink_value)
    wikiurl_value = wikiurl.sub(r"<a href='\2'>\1</a>", wikiotherlink_value)
    youtube_value = youtubelink.sub(r'<iframe width="560" height="315" src="https://www.youtube.com/embed/\1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', wikiurl_value)
    return youtube_value
