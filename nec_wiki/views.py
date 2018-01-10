from django.shortcuts import render
from .models import Page
from django.http import HttpResponseRedirect
import markdown

# Create your views here.
def view_page(request, user_name, page_name):
    if request.user.is_authenticated and request.user.username == user_name:
        try:
            page = Page.objects.get(title=page_name, owner=request.user)
        except Page.DoesNotExist:
            return render(request, 'nec_wiki/create_page.html', {'user_name':user_name, 'page_name':page_name})
        content = page.content
        return render(request, 'nec_wiki/view_page.html', {'user_name':user_name, 'page_name':page_name, 'content':content, 'markdown':markdown.markdown(content)})
    else:
        return redirect(settings.LOGIN_URL)

def edit_page(request, user_name, page_name):
    if request.user.is_authenticated and request.user.username == user_name:
        try:
            page = Page.objects.get(title=page_name, owner=request.user)
            content = page.content
        except:
            content = ""
        return render(request, 'nec_wiki/edit_page.html', {'user_name':user_name, 'page_name':page_name, 'content':content})
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
        return HttpResponseRedirect("/wiki/" + user_name + "/" + page_name + "/")
    else:
        return redirect(settings.LOGIN_URL)

def dashboard_page(request, user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        page_list = Page.objects.all()
        return render(request, 'nec_wiki/dashboard_page.html', {'user_name':user_name, 'page_list':page_list})
    else:
        return redirect(settings.LOGIN_URL)
