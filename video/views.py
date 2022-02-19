from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, resolve_url, get_object_or_404
from django.views.generic import View, CreateView, ListView
from .models import Video, Category
from .forms import Video_post, LoginForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_
from django.core.paginator import Paginator


class OnlyMyPostMixin(UserPassesTestMixin):
    raise_excption = True
    def test_func(self):
        post = Video.objects.get(id=self.kwargs['pk'])
        return post.author == self.request.user

def top_page(request):
    return render(request, 'video/top_page.html', {})


class IndexView(ListView):
    def get(self, request, *args, **kwargs):
        video = Video.objects.all().order_by('-id')
        paginator = Paginator(Video.objects.all().order_by('-id'), 5)
        video_page = request.GET.get('page')
        videos = paginator.get_page(video_page)

        return render(request, 'video/index.html', {
            'video': video,
            'videos': videos
        })


class VideoDetailView(View):
    def get(self, request, *args, **kwargs):
        post_video = Video.objects.get(id=self.kwargs['pk'],)
        return render(request, 'video/video_detail.html', {
            'post_video': post_video
        })


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Video

    def get(self, request, *args, **kwargs):
        form = Video_post(data=request.POST, files=request.FILES)
        success_url = reverse_lazy('/video/index')

        return render(request, 'video/video_post.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = Video_post(data=request.POST, files=request.FILES)

        # if request.method == "POST" and form.is_valid():
        if form.is_valid():
            post_data = Video()
            post_data.author = request.user
            post_data.caption = form.cleaned_data['caption']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            # if request.FILES:
            #     post_data.video = request.FILES.get('video')
            post_data.video = request.FILES['video']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('/video/index/')

        return render(request, 'video/video_post.html', {
            'form': form
        })



class PostEditView(OnlyMyPostMixin, CreateView):
    def get(self, request, *args, **kwargs):
        post_data = Video.objects.get(id=self.kwargs['pk'])
        form = Video_post(
            request.POST or None,
            initial={
                'author': post_data.author,
                'caption': post_data.caption,
                'category': post_data.category,
                'video': post_data.video,
                'content': post_data.content,
            })
        return render(request, 'video/video_post.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = Video_post(data=request.POST, files=request.FILES)

        if form.is_valid():
            post_data = Video.objects.get(id=self.kwargs['pk'])
            post_data.caption = form.cleaned_data['caption']
            if request.FILES:
                post_data.video = request.FILES.get('video')
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('/video/index/', self.kwargs['pk'])

        return render(request, 'video/video_post.html', {
            'form': form
        })


class PostDeleteView(OnlyMyPostMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Video.objects.get(id=self.kwargs['pk'])
        return render(request, 'video/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Video.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('/video/index/')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'video/login.html'

    def get_success_url(self):
        messages.success(self.request, 'ログインしました')
        return resolve_url('video:index')


class Logout(LogoutView):
    template_name = 'video/logout.html'

    def get_success_url(self):
        messages.warning(self.request, 'ログアウトしました')
        return resolve_url('video:top_page')



class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'video/signup.html'
    success_url = reverse_lazy('video:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.info(self.request, 'ユーザー登録しました')
        return HttpResponseRedirect(self.get_success_url())


def search(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        videos = Video.objects.order_by('-id').filter(content__contains=keyword)
        return render(request, 'video/index.html', {
            'keyword': keyword,
            'videos': videos
        })
    else:
        return render(request, 'video/index.html', {})


class AddCategoryView(CreateView):
    model = Category
    template_name = 'video/category_list.html'
    fields = '__all__'

    def get_success_url(self):
        messages.warning(self.request, 'カテゴリ追加しました')
        return resolve_url('video:index')

#
# def CategoryView(request, category):
#     if request.method == 'GET':
#         # category = get_object_or_404(Category, name=category)
#         category = Category.objects.get(name=category)
#         # category_post = Video.objects.all().order_by('-id').filter(name=category)
#         category_post = Video.objects.all().filter(category=category)
#         return render(request, 'video/categories.html', {
#             'category': category,
#             'category_post': category_post
#         })
#     else:
#         return render(request, 'video/index.html', {})


def CategoryView(request, category):
    if request.method == 'GET':
        # category = get_object_or_404(Category, name=category)
        category = Category.objects.get(name=category)
        category_post = Video.objects.all().order_by('-id').filter(category=category)
        return render(request, 'video/categories.html', {
            'category': category,
            'category_post': category_post
        })

    else:
        return render(request, 'video/index.html', {})



# class CategoryView(View):
#     def get(self, request, *args, **kwargs):
#         category_data = Category.objects.get(name=self.kwargs['category'])
#         post_data = Video.objects.order_by('-id').filter(category=category_data)
#         return render(request, 'video/index.html', {
#             'post_data': post_data
#         })
