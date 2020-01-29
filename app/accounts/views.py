from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm

from accounts.forms import MyUserCreationForm


class UserSignUpView(TemplateView):

    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = MyUserCreationForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LogInView(TemplateView):

    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request,
                username=username,
                password=password
                )
            login(request, user)
            if user.is_teacher:
                return redirect('quiz:teacher_cabinet')
            elif user.is_student:
                return redirect('quiz:student_class')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LogOutView(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('accounts:login')
