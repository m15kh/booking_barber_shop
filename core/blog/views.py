from typing import Any, Optional
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView , DeleteView
from django.views.generic.detail import SingleObjectMixin # new
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm, CommentForm
from django.views import View


class CommentGet(DetailView):
    model = Post
    template_name = 'blog/detail_post.html'
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class CommentPost( SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/detail_post.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user  # Set the author to the logged-in user
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        post = self.get_object()
        return reverse("blog:detail_post", kwargs={"pk": post.pk})
    


class PostViewDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)




class PostViewList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/all_post.html'
    login_url = 'login'


        
class PostViewNew(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/new_post.html'
    reverse_lazy = 'blog:all_post'
    login_url = 'login'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostViewEdit(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/edit_post.html'
    login_url = 'login'
    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser


class PostViewDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:all_post')
    login_url = 'login'

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser
