from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task, CustomUser
from .forms import CustomUserCreationForm, TaskForm
from datetime import date

# Home page
def index(request):
    return render(request, 'website/index.html')

# User Signup
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # ✅ Redirect to login after signup
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'website/signup.html', {'form': form})


# Task List with Filtering
@login_required
def task_list(request):
    filter_option = request.GET.get('filter', 'all')
    tasks = Task.objects.filter(user=request.user)

    filter_map = {
        'pending': tasks.filter(status='pending'),
        'completed': tasks.filter(status='completed'),
        'due_today': tasks.filter(due_date=date.today())
    }

    tasks = filter_map.get(filter_option, tasks)
    return render(request, 'website/task_list.html', {'tasks': tasks})

# Create New Task
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'website/task_form.html', {'form': form})

# Edit Task
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'website/task_form.html', {'form': form})

# Delete Task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'website/task_confirm_delete.html', {'task': task})

# Toggle Task Status
@login_required
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = 'completed' if task.status == 'pending' else 'pending'
    task.save()
    return redirect('task_list')


from django.contrib.auth import logout

def custom_logout_view(request):
    logout(request)
    return redirect('index')  # ✅ Redirect users to home after logout
