from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import TodoForm, TodoFilterForm
from .models import Todo

# Create your views here.

def homeView(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task Added To Todo List Successfully!')
            return redirect(homeView)
    else:
        form = TodoForm()

    filter_form = TodoFilterForm(request.POST or None)
    if filter_form.is_valid():
        filter_status = filter_form.cleaned_data['status']
        if filter_status == 'all':
            todoList = Todo.objects.all().order_by('completed')
        elif filter_status == 'completed':
            todoList = Todo.objects.filter(completed=True)
        else:
            todoList = Todo.objects.filter(completed=False)
    else:
        todoList = Todo.objects.all().order_by('completed')

    return render (request, 'todo/index.html', context={
        'todoList':todoList,
        'form':form,
        'filter_form':filter_form
    })

def completeTaskView(request, id):
    task = get_object_or_404(Todo, id=id)
    if task.completed:
        task.completed = False
        messages.error(request, 'Marked Task As Uncompleted.')
    else:
        task.completed = True
        messages.success(request, 'Marked Task As Completed.')
    task.save()
    return redirect(homeView)

def editTaskView(request, id):
    task = get_object_or_404(Todo, id=id)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.info(request, 'Task Edited')
            return redirect(homeView)
    else:
        form = TodoForm(instance=task)
    todoList = Todo.objects.all().order_by('completed').exclude(id=id)
    return render (request, 'todo/index.html', context={
        'todoList':todoList,
        'form':form
    })

def deleteTaskView(request, id):
    task = get_object_or_404(Todo, id=id)
    task.delete()
    messages.error(request, 'Task Deleted.')
    return redirect(homeView)

def deleteAllTaskView(request):
    BATCH_SIZE = 100
    for task in Todo.objects.iterator(chunk_size=BATCH_SIZE):
        task.delete()
    messages.error(request, 'All Task Deleted.')
    return redirect(homeView)
