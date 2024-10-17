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
from django.contrib import messages


class TodoList(LoginRequiredMixin, ListView):
    template_name = 'todo_list.html'
    model = Todo
    context_object_name = "tasks"
    login_url = '/accounts/user_login/'

    def get_queryset(self):
        queryset = Todo.objects.filter(user=self.request.user)
        
        sort = self.request.GET.get('sort', None)
        if sort == 'urgency':
            queryset = queryset.order_by('-urgency')  
        elif sort == 'importance':
            queryset = queryset.order_by('-importance')

        urgency_filter = self.request.GET.get('urgency', None)
        if urgency_filter:
            queryset = queryset.filter(urgency=urgency_filter)

        importance_filter = self.request.GET.get('importance', None)
        if importance_filter:
            queryset = queryset.filter(importance=importance_filter)

        title_filter = self.request.GET.get('title', None)
        if title_filter:
            queryset = queryset.filter(title__icontains=title_filter)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context
    
    def handle_no_permission(self):
        messages.warning(self.request, 'ログインしてください')
        return redirect(self.get_login_url())

class TodoDetail(LoginRequiredMixin, DetailView):
    template_name = 'todo_detail.html'
    model = Todo
    context_object_name = "task"
    login_url = '/accounts/user_login/'

    def handle_no_permission(self):
        messages.warning(self.request, 'ログインしてください')
        return redirect(self.get_login_url())

class TodoCreate(LoginRequiredMixin, CreateView):
    template_name = 'todo_form.html'
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy("accounts:list")
    login_url = '/accounts/user_login/'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def handle_no_permission(self):
        messages.warning(self.request, 'ログインしてください')
        return redirect(self.get_login_url())

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'todo_update.html'
    model = Todo
    fields = ['title', 'description', 'deadline', 'urgency', 'importance']
    success_url = reverse_lazy("accounts:list")
    login_url = '/accounts/user_login/'

    def handle_no_permission(self):
        messages.warning(self.request, 'ログインしてください')
        return redirect(self.get_login_url())
    
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)
    
class TodoDelete(LoginRequiredMixin, DeleteView):
    template_name = 'todo_confirm_delete.html'
    model = Todo
    context_object_name = "task"
    success_url = reverse_lazy("accounts:list")
    login_url = '/accounts/user_login/'

    def handle_no_permission(self):
        messages.warning(self.request, 'ログインしてください')
        return redirect(self.get_login_url())

class HomeView(TemplateView):
    template_name = 'home.html'

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:home')
    def form_valid(self, form):
        user = form.save(commit=True)  
        login(self.request, user) 
        return super().form_valid(form)

class UserLoginView(FormView):
    template_name = 'user_login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        next_url = request.POST.get('next', 'accounts:home') 

        if user is not None and user.is_active:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'ログインに失敗しました。')
            return self.form_invalid(self.get_form())


class UserLogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:home')

class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)