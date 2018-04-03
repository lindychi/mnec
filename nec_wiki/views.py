from django.shortcuts import render, redirect, get_object_or_404
from .models import Page, Tag
import markdown
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import PageForm, TagForm


@login_required(login_url=settings.LOGIN_URL)
def index(request):
    page_list = Page.objects.all()
    return render(request, 'nec_wiki/dashboard.html', {'page_list': page_list})


@login_required(login_url=settings.LOGIN_URL)
def view_page(request, page_name):
    try:
        page = Page.objects.get(title=page_name, owner=request.user)
    except Page.DoesNotExist:
        return render(request, 'nec_wiki/no_page.html',
                      {'page_name': page_name})
    content = page.content
    return render(request, 'nec_wiki/view_page.html',
                  {'content': markdown.markdown(content), 'page': page})


@login_required(login_url=settings.LOGIN_URL)
def view_other_page(request, user_name, page_name):
    try:
        page = Page.objects.get(title=page_name, owner=request.user)
        tags = page.tags.all()
    except Page.DoesNotExist:
        return render(request, 'nec_wiki/no_page.html',
                      {'user_name': user_name, 'page_name': page_name})
    content = page.content
    return render(request, 'nec_wiki/view_page.html',
                  {'user_name': user_name, 'page_name': page_name,
                   'content': markdown.markdown(content), 'tags': tags, 'page':page})

@login_required(login_url=settings.LOGIN_URL)
def edit_page(request, user_name, page_name):
    """Edit page.

    url with user_name, page_name
    user_name: unique
    page_name: not unique

    user can only access user's own pages
    """
    try:
        page = Page.objects.get(owner=request.user, title=page_name)
    except Page.DoesNotExist:
        page = Page(owner=request.user, title=page_name)
        page.save()
    if request.method == 'POST':
        page_form = PageForm(request.POST, request.FILES, instance=page)
        if page_form.is_valid():
            page.save_form(page_form)
            return redirect(page)
        else:
            return render(request, 'nec_wiki/edit_page.html',
                          {'page': page, 'page_form': page_form})
    else:
        page_form = PageForm(instance=page)
        return render(request, 'nec_wiki/edit_page.html',
                      {'page': page, 'page_form': page_form})


@login_required(login_url=settings.LOGIN_URL)
def create_page(request, user_name):
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page = Page(owner=request.user)
            page.save() #for set id
            page.save_form(form)
            return redirect(page)
        else:
            return render(request, 'nec_wiki/create_page.html',
                          {'page_form': form})
    else:
        form = PageForm()
        return render(request, 'nec_wiki/create_page.html',
                      {'page_form': form})


@login_required(login_url=settings.LOGIN_URL)
def create_tag(request, user_name):
    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            tag = form.save(request.user)
            return redirect(tag)
        else:
            return render(request, 'nec_wiki/create_tag.html',
                          {'tag_form': form})
    else:
        form = TagForm()
        return render(request, 'nec_wiki/create_tag.html', {'tag_form': form})


@login_required(login_url=settings.LOGIN_URL)
def delete_page(request, user_name, page_name):
    return None


@login_required(login_url=settings.LOGIN_URL)
def view_tag(request, user_name, tag_name):
    try:
        tag = Tag.objects.get(name=tag_name, owner=request.user)
        pages = tag.page_set.all()
    except Tag.DoesNotExist:
        tag = None
        pages = []
    return render(request, 'nec_wiki/view_tag.html',
                  {'user_name': user_name,
                   'tag_name': tag_name,
                   'pages': pages})
