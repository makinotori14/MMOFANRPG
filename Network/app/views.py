from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from .models import Category, Post, Reply, FileKeep
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .filters import PostFilter
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

class HomeView(TemplateView):
    template_name = 'home.html'

#POSTS

class PostList(ListView):
    model = Post
    template_name = 'Post/list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-time_of_creation']

class PostCreate(LoginRequiredMixin, TemplateView):
    template_name = 'Post/create.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        category = Category.objects.get(name=request.POST['category'])

        post = Post(
            author=user,
            category=category,
            title=request.POST['title'],
            text=request.POST['text'],
        )
        post.save()
        files = request.FILES.getlist('files')
        for f in files:
            FileKeep.objects.create(files=f, post=post)

        return redirect('/posts/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'Post/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = FileKeep.objects.filter(post=super().get_object())
        return context

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'Post/update.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get(self, request, *args, **kwargs):
        if self.request.user != super().get_object().author:
            raise PermissionDenied()
        return super(PostUpdate, self).get(request, *args, **kwargs)

class MyPostList(ListView):
    model = Post
    template_name = 'Post/mylist.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

#Reply views

class ReplyCreate(LoginRequiredMixin, TemplateView):
    template_name = 'Reply/create.html'

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)

        reply = Reply(
            post=post,
            text=request.POST['text'],
            author=self.request.user
        )
        reply.save()

        send_mail(
            subject='На ваше объявление ответили!',
            message=f'На объявление {post.title} ответили!\nhttp://localhost:8000/myreplies/{reply.pk}/',
            from_email='mmofanrpg@yandex.ru',
            recipient_list=[reply.post.author.email]
        )

        return redirect(f'/posts/{id}/')
    
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        if self.request.user == post.author:
            raise PermissionDenied()
        return super(ReplyCreate, self).get(request, *args, **kwargs)

class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'Reply/list.html'
    context_object_name = 'replies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
    def get_queryset(self):
        return Reply.objects.filter(post__author=self.request.user, status=False)

class ReplyDetail(LoginRequiredMixin, DetailView):
    model = Reply
    template_name = 'Reply/detail.html'
    context_object_name = 'reply'

    def get(self, request, *args, **kwargs):
        if self.request.user != super().get_object().post.author:
            raise PermissionDenied()
        return super(ReplyDetail, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        reply = super().get_object()
        reply.accept()
        send_mail(
            subject='Ваш отклик был принят!',
            message=f'Ваш отклик на пост {reply.post.text[:50]} был принят!',
            from_email='mmofanrpg@yandex.ru',
            recipient_list=[reply.author.email]
        )
        return redirect(f'/myreplies/{id}/')

class ReplyDelete(LoginRequiredMixin ,DeleteView):
    template_name = 'Reply/delete.html'
    queryset = Reply.objects.all()
    success_url = '/myreplies/'

    def get(self, request, *args, **kwargs):
        reply = super().get_object()
        if self.request.user != reply.post.author or reply.status:
            raise PermissionDenied()
        return super(ReplyDelete, self).get(request, *args, **kwargs)

#MAILING

class Mailing(TemplateView):
    template_name = 'mailing.html'

    def post(self, request, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            send_mail(
                subject=request.POST['subject'],
                message=request.POST['message'],
                from_email='mmofanrpg@yandex.ru',
                recipient_list=[user.email]
            )
        return redirect('/home/')

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied()
        return super().get(request)
