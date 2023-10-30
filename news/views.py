from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy, resolve
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.conf import settings

from .models import Post, Author, Category
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import QuerySet
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


class PostList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'

    paginate_by = 10

    def get_queryset(self) -> QuerySet(any):
        post_filter = PostFilter(self.request.GET, queryset=Post.objects.all())
        return post_filter.qs.order_by('-dateCreation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'news/new_detail.html'
    context_object_name = 'news'
    queryset = Post.objects.all()


class News(View):

    def get(self, request):
        news = Post.objects.order_by('-dateCreation')
        p = Paginator(news, 1)
        news = p.get_page(
            request.GET.get('page', 1))

        data = {
            'news': news,
        }

        return render(request, 'news/search.html', data)


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news/new_create.html'
    form_class = PostForm
    context_object_name = 'news'
    permission_required = ('news.add_post', 'news.view_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news/new_create.html'
    form_class = PostForm
    context_object_name = 'news'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/new_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:news')
    context_object_name = 'news'


class PostCategoryView(ListView):
    model = Post
    template_name = 'news/category.html'
    context_object_name = 'news'
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_queryset(self):
        self.id = self.kwargs.get('pk')
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['category'] = category
        return context


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'{category} subcription',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email, ],
        )
        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('news:news')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect('protect:index')


def CategoryDetailView(request, pk):
    category = Category.objects.get(pk=pk)
    is_subscribed = True if len(category.subscribers.filter(id=request.user.id)) else False

    return render(request, 'news/category.html',
                  {'category': category,
                   'is_subscribed': is_subscribed,
                   'subscribers': category.subscribers.all()
                   })


def get_subscribers(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email


def new_post_subscriptions(instance):
    template = 'mail/new_post.html'

    for category in instance.category.all():
        email_subject = f'Новая публикация в категории "{category}"'
        user_emails = get_subscribers(category)
        html = render_to_string(
            template_name=template,
            context={
                'category': category,
                'post': instance,
            }
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_emails,
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
