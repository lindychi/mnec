from django import template

register = template.Library()

# @register.inclusion_tag('project_detail.html')
# def show_childs(todo):
#     childs = todo.child.all()
#     return {'childs':childs}

@register.filter
def indent(depth):
    ind = ""
    for a in range(depth):
        ind += "　　"
    return ind

@register.inclusion_tag('project/child.html')
def show_childs(todo):
    childs = todo.child.order_by('-priority')
    return {'childs':childs}