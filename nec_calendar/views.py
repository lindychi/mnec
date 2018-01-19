from django.shortcuts import render
import re
import logging

day_parse = re.compile("\<td\sclass=\"(\S+)\"\>([^\<]*)\<\/td\>")


# Create your views here.
class Calendar:
    token_list = None
    size = 0

    def __init__(self, html):
        print(html)
        token_list = day_parse.match(html).groups()
        print(token_list)
        size = token_list.size()

    def get_size(self):
        return self.size


def index(request):
    return None
