from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'todo/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

def task_list(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    tasks = Task.objects.all()
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def add_task(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'todo/add_task.html', {'form': form})

def edit_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login/')
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'todo/add_task.html', {'form': form})

def delete_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login/')
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('/')