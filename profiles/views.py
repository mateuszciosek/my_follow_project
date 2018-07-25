from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic import (
    CreateView, TemplateView,
    DetailView, UpdateView,
    ListView,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Profile
from .forms import (
    UserUpdateAccount, UserUpdateProfile,
    UserCreateForm,
)


class Register(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('success')
    template_name = 'index.html'


class UserProfile(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    template_name = 'user_profile.html'


class SuccessRegister(TemplateView):
    template_name = 'success_login.html'


class ProfileDetails(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    model = User
    context_object_name = 'this_user'
    slug_field = "username"
    template_name = 'profile_details.html'


class UserList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    model = User
    template_name = 'user_list.html'

    def get_queryset(self):
        return self.model.objects.exclude(username=self.request.user.username)


class RequestListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    model = User
    context_object_name = 'request_list'
    template_name = "request_follow_list.html"


@login_required(redirect_field_name='index.html', login_url='/login/')
def edit_account(request):
    if request.method == "POST":
        user_form = UserUpdateAccount(request.POST, instance=request.user)
        profile_form = UserUpdateProfile(
            request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/profile/details')
    else:
        user_form = UserUpdateAccount(instance=request.user)
        profile_form = UserUpdateProfile(
            request.POST, instance=request.user.profile)
        args = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_account_edit.html', args)


def add_follow(request, pk):
    user_to_follow = get_object_or_404(Profile, pk=pk)
    user_to_follow.request_follows.add(request.user.profile)
    user_to_follow.save()
    request.user.profile.follow(user_to_follow)
    request.user.profile.save()
    return redirect('profile_details', slug=user_to_follow.user.username)


def unfollow(request, pk):
    user_to_unfollow = get_object_or_404(Profile, pk=pk)
    request.user.profile.accepted_follows.remove(user_to_unfollow)
    request.user.profile.save()
    return redirect('profile_details', slug=user_to_unfollow.user.username)


def cancel_request(request, pk):
    user_to_follow = get_object_or_404(Profile, pk=pk)
    request.user.profile.follows.remove(user_to_follow)
    request.user.profile.save()
    user_to_follow.request_follows.remove(request.user.profile)
    user_to_follow.save()
    return redirect('profile_details', slug=user_to_follow.user.username)


def accept_follow(request, pk):
    user_to_accept = get_object_or_404(Profile, pk=pk)
    user_to_accept.follows.remove(request.user.profile)
    user_to_accept.accepted_follows.add(request.user.profile)
    user_to_accept.save()
    request.user.profile.request_follows.remove(user_to_accept)
    request.user.profile.save()
    return redirect('request_follow_list')
