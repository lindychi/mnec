from django.shortcuts import render, redirect, get_object_or_404
from .models import Page, Tag
from django.http import HttpResponseRedirect
import markdown
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import PageForm, TagForm
import copy


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('wiki_dashboard', args=(request.user.username,)))
    else:
        return redirect(settings.LOGIN_URL)


def view_page(request, user_name, page_name):
    if request.user.is_authenticated and request.user.username == user_name:
        try:
            page = Page.objects.get(title=page_name, owner=request.user)
            tags = page.tags.all()
        except Page.DoesNotExist:
            return render(request, 'nec_wiki/no_page.html', {'user_name':user_name, 'page_name':page_name})
        content = page.content
        return render(request, 'nec_wiki/view_page.html', {'user_name':user_name, 'page_name':page_name, 'content':markdown.markdown(content), 'tags':tags})
    else:
        return redirect(settings.LOGIN_URL)


@login_required(login_url=settings.LOGIN_URL)
def edit_page(request, user_name, page_name):
    try:
        page = Page.objects.get(owner=request.user, title=page_name)
    except Page.DoesNotExist:
        return render(request, 'nec_wiki/no_page.html', {'page_name': page_name})
    if request.method == 'POST':
        page_form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            page = form.save()
            return redirect(page)
        else:
            return render(request, 'nec_wiki/edit_page.html', {'page': page, 'page_form': page_form})
    else:
        page_form = PageForm(instance=page)
        return render(request, 'nec_wiki/edit_page.html', {'page': page, 'page_form': page_form})


def save_new_page(request, user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        content = request.POST["content"]
        page_name = request.POST["title"]
        page = Page(owner=request.user, title=page_name, content=content)
        page.save()
        page.setTags(request.POST["tags"])
        return HttpResponseRedirect(reverse('wiki_view_page', args=(user_name, page_name,)))
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
        page.setTags(request.POST["tags"])
        return HttpResponseRedirect(reverse('wiki_view_page', args=(user_name, page_name,)))
    else:
        return redirect(settings.LOGIN_URL)


def dashboard(request, user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        page_list = Page.objects.all()
        return render(request, 'nec_wiki/dashboard.html', {'user_name':user_name, 'page_list':page_list})
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
