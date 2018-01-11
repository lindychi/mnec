from django.shortcuts import render, redirect
from .models import Page, Tag
from django.http import HttpResponseRedirect
import markdown
from django.conf import settings
from django.urls import reverse

# Create your views here.
def index_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard_wiki_page', args=(request.user.username,)))
    else:
        return redirect(settings.LOGIN_URL)

def view_page(request, user_name, page_name):
    if request.user.is_authenticated and request.user.username == user_name:
        try:
            page = Page.objects.get(title=page_name, owner=request.user)
            tags = page.tags.all()
        except Page.DoesNotExist:
            return render(request, 'nec_wiki/create_page.html', {'user_name':user_name, 'page_name':page_name})
        content = page.content
        return render(request, 'nec_wiki/view_page.html', {'user_name':user_name, 'page_name':page_name, 'content':markdown.markdown(content), 'tags':tags})
    else:
        return redirect(settings.LOGIN_URL)

def edit_page(request, user_name, page_name):
    if request.user.is_authenticated and request.user.username == user_name:
        try:
            page = Page.objects.get(title=page_name, owner=request.user)
            content = page.content
            tags = page.tags.all()
        except Page.DoesNotExist:
            content = ""
        return render(request, 'nec_wiki/edit_page.html', {'user_name':user_name, 'page_name':page_name, 'content':content, 'tags':tags})
    else:
        return redirect(settings.LOGIN_URL)

def save_new_page(request, user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        content = request.POST["content"]
        page_name = request.POST["title"]
        page = Page(owner=request.user, title=page_name, content=content)
        page.save()

        if "tags" in request.POST:
            page.setTags(request.POST["tags"])
        return HttpResponseRedirect("/wiki/" + user_name + "/" + page_name + "/")
    else:
        return redirect(settings.LOGIN_URL)

def save_page(request, user_name, page_name):
    if request.user.is_authenticated and request.user.username == user_name:
        content = request.POST["content"]
        try:
            page = Page.objects.get(title=page_name, owner=request.user)
            page.content = content
        except Page.DoesNotExist:
            page = Page(owner=request.user, title=page_name, content=content)
        page.save()

        if "tags" in request.POST:
            page.setTags(request.POST["tags"])
        return HttpResponseRedirect(reverse('view_wiki_page', args=(user_name, page_name,)))
    else:
        return redirect(settings.LOGIN_URL)

def dashboard_page(request, user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        page_list = Page.objects.all()
        return render(request, 'nec_wiki/dashboard_page.html', {'user_name':user_name, 'page_list':page_list})
    else:
        return redirect(settings.LOGIN_URL)

def create_page(request, user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        return render(request, 'nec_wiki/create_page.html', {'user_name':user_name})
    else:
        return redirect(settings.LOGIN_URL)

def delete_page(request, user_name, page_name):
    return None

def view_tag(request, user_name, tag_name):
    try:
        tag = Tag.objects.get(name=tag_name, owner=request.user)
        pages = tag.page_set.all()
    except Tag.DoesNotExist:
        tag = None
        pages = []
    return render(request, 'nec_wiki/view_tag.html', {'user_name':user_name, 'tag_name':tag_name, 'pages':pages})
