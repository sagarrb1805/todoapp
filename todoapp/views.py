# from urllib import request
from django.shortcuts import render, redirect
from .models import Task
from . froms import TaskForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        context = {'usrname':username, 'eamil':email}
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username not avialble choose different one')
            return render(request, 'register.html', {'username':username, 'email':email})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with same email already exits try login')
            return redirect('/')
        if password1 != password2:
            messages.error(request, "password doesn't match")
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "account created succesfully try login.")
        return redirect('/')
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
        except:
            user = None
        if user is not None:
            login(request, user)
            return redirect('todoapp:TaskListView')
        else:
            messages.error(request, 'Invalid credentials try again.')
            return redirect('/')
    return render(request, 'index.html')

@login_required
def TaskListView(request):
    tasks = Task.objects.filter(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('task')
        priority = request.POST.get('priority')
        date = request.POST.get('date')
        user = request.user
        task = Task(user=user, name=name, priority=priority, date=date)
        task.save()
        return redirect('todoapp:TaskListView')
    return render(request, 'home.html', {'tasks':tasks})

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'task'
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'updateview.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('todoapp:TaskDetailView', kwargs={'pk':self.object.id})
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:TaskListView')





# def delete(request, task_id):
#     task = Task.objects.get(id=task_id)
#     if request.method == 'POST':
#         task.delete()
#         return redirect('/')
#     return render(request, 'delete.html')

# def update_task(request, task_id):
#     task = Task.objects.get(id=task_id)

#     form = TaskForm(request.POST or None, instance=task)
#     if form.is_valid():
#         form.save()
#         return redirect('/')

#     return render (request, 'update.html', {'task': task, 'form': form})






# def update_task(request, task_id):
#     task = Task.objects.get(id=task_id)

#     if request.method == "POST":
#         name = request.POST.get('task', '')
#         priority = request.POST.get('priority', '')
#         date = request.POST.get('date', '')
#         task.name = name
#         task.priority = priority
#         task.date = date
#         task.save()
#         return redirect('/')
#     return render(request, 'update.html', {'task': task})


