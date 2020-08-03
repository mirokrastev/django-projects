from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task
from django.utils import timezone


def home_view(request, error=None):
    todos = None
    if request.user.is_authenticated:
        todos = Task.objects.filter(user=request.user, date_completed__isnull=True).order_by('-date_created')
    return render(request, 'home.html', {'todos': todos, 'message': error})


def get_object(request, task_pk):
    try:
        return Task.objects.get(pk=task_pk, user=request.user)
    except (Task.DoesNotExist, ValueError):
        return None


@login_required
def completed_todos_view(request):
    todos = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_created')
    return render(request, 'home.html', {'todos': todos})


@login_required
def create_todo_view(request):
    error = None

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if len(form['title'].data) <= 50:
            new = form.save(commit=False)
            new.user = request.user
            new.save()

            return redirect('home')

        error = 'Please submit only valid data.'
    form = TaskForm()
    return render(request, 'todolist/create_todo.html', {'form': form, 'error': error})


@login_required
def detailed_todo_view(request, task_pk):
    task = get_object(request, task_pk)
    if not task:
        return home_view(request, 'Invalid task.')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        form.save()
    task_paragraph = TaskForm(instance=task)
    return render(request, 'todolist/detailed_todo.html', {'object': task, 'task': task_paragraph})


@login_required
def complete_todo_view(request, task_pk):
    task = get_object(request, task_pk)
    if not task:
        return home_view(request, 'Invalid task.')

    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return render(request, 'home.html', {'message': f'You completed task {task.title}!'})
    return redirect(home_view)


@login_required
def delete_todo_view(request, task_pk):
    task = get_object(request, task_pk)
    if not task:
        return home_view(request, 'Invalid task.')

    if request.method == 'POST':
        task.delete()
        return render(request, 'home.html', {'message': f'You deleted task {task.title}!'})
    return redirect(home_view)