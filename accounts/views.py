from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView,  DeleteView
from django.urls import reverse_lazy
from .models import Todo
from django.utils import timezone
from .forms import TodoForm


class TodoList(ListView):
    template_name = 'todo_list.html'
    model = Todo
    context_object_name = "tasks"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context

class TodoDetail(DetailView):
    template_name = 'todo_detail.html'
    model = Todo
    context_object_name = "task"

class TodoCreate(CreateView):
    template_name = 'todo_form.html'
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy("accounts:list")

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class TodoUpdate(UpdateView):
    template_name = 'todo_form.html'
    model = Todo
    fields = "__all__"
    success_url = reverse_lazy("accounts:list")

class TodoDelete(DeleteView):
    template_name = 'todo_confirm_delete.html'
    model = Todo
    context_object_name = "task"
    success_url = reverse_lazy("accounts:list")

class HomeView(TemplateView):
    template_name = 'home.html'

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm

class UserLoginView(FormView):
    template_name = 'user_login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        next_url = request.POST['next']
        if user is not None and user.is_active:
            login(request, user)
        if next_url:
            return redirect(next_url)
        return redirect('accounts:home')

class UserLogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:user_login')

class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)