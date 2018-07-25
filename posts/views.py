from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView,
    UpdateView, CreateView,
    DeleteView,
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.models import Profile
from django.contrib.auth.models import User

from .models import Post, Comment
from .forms import (
    PostForm, CommentForm,
    EditPostForm,
)

import lxml.etree


class FollowersPostListView(LoginRequiredMixin, ListView):
    login_url = '/'
    redirect_field_name = 'index.html'

    model = Post
    template_name = "dashboard.html"

    def get_queryset(self):
        return Post.objects.filter(
            author__in=self.request.user.profile.accepted_follows.all().values_list('id')
        ).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super(FollowersPostListView, self).get_context_data(**kwargs)
        context['follow_users'] = User.objects.filter(
            profile__in=self.request.user.profile.accepted_follows.all().values_list('id')
        )
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'post_detail.html'

    form_class = PostForm
    template_name = 'add_post_form.html'
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


class UserPostListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    model = Post
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'user_posts.html'

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).order_by('-created_date')


class AnotherUserPostListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    model = Post
    template_name = 'user_post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_success_url(self):
        username = self.kwargs['username']
        return reverse('user_post_list', kwargs={'username': username})

    def get_queryset(self):
        return self.model.objects.filter(author_id=self.kwargs['pk'])


class PostDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    model = Post


class PostEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    template_name = "post_edit.html"
    form_class = EditPostForm
    model = Post

    def get_queryset(self):
        base_qs = super(PostEdit, self).get_queryset()
        return base_qs.filter(author=self.request.user)


class PostRemove(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    template_name = 'post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('user_posts')

    def get_queryset(self):
        base_qs = super(PostRemove, self).get_queryset()
        return base_qs.filter(author=self.request.user)


@login_required(redirect_field_name='index.html', login_url='/login/')
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})


def show_game_list(request, game_name):
    tree = lxml.etree.parse(
        'http://thegamesdb.net/api/GetGamesList.php?name={}'.format(game_name))
    games = tree.xpath("//Game")
    game_list = []

    for game in games:
        game_title = game.find("GameTitle").text
        game_list.append(game_title)

    context = {
        'game_list': game_list
    }
    return render(request, 'game_list.html', context)
