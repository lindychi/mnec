from django.shortcuts import render
from .models import Todo
from django.utils import timezone

# Create your views here.
def index_page(request):
    if request.user.is_authenticated:
        todolists = Todo.objects.filter(owner=request.user, created_date__lte=timezone.now()).order_by('-created_date')
        return render(request, 'nec_todo/index.html', {'todolists':todolists})
    else:
        return redirect(settings.LOGIN_URL)
