from typing import Any, Optional
from django.db import models
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.translation import gettext as _
from .models import Profile
from .forms import ProfileForm

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "myauth/user_list.html"

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "myauth/profile_detail.html"

class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "myauth/profile_form.html"

    def test_func(self) -> bool | None:
        user = self.request.user
        cur_user = self.get_object().user
        return user.is_staff or (user.pk == cur_user.pk)
    
    def get_success_url(self) -> str:
        return reverse("myauth:profile_detail", kwargs={"pk": self.object.pk})

    #def form_valid(self, form) -> HttpResponse:
    #    response = super().form_valid(form)
    #    profile, created = Profile.objects.get_or_create(user=self.object)
    #    if form.files.get("avatar"):
    #        profile.avatar = form.files.get("avatar")
    #    if form.cleaned_data.get("bio"):
    #        profile.bio = form.cleaned_data.get("bio")
    #    if form.cleaned_data.get("birthday"):
    #        profile.birthday = form.cleaned_data.get("birthday")
    #    if form.cleaned_data.get("agreement_accepted"):
    #        profile.agreement_accepted = form.cleaned_data.get("agreement_accepted")
    #    profile.save()
    #    return response

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "myauth/profile.html"

class AboutMeView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = "avatar", 
    template_name = "myauth/about-me.html"
    success_url = reverse_lazy("myauth:about_me")

    def get_object(self, queryset = None):
        profile, created = self.model.objects.get_or_create(user=self.request.user)
        return profile

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user=user)
        return response

class MyLoginView(LoginView):
    template_name = "myauth/login.html"
    redirect_authenticated_user = True

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

@login_required
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'Неизвестный пользователь'
    response = HttpResponse("Set cookie")
    response.set_cookie("UserName", username, max_age=3600)
    return response

@login_required
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("UserName", "Значение пока не задано")
    return HttpResponse(f'Cookie value: {value!r}')

@login_required
def set_session_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'Неизвестный пользователь'
    request.session["UserName"] = username
    return HttpResponse("Set session")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("UserName", "Значение пока не задано")
    return HttpResponse(f'Session value: {value!r}')