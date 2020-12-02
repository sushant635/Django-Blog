from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from blog.models import Post,Comment
from blog.forms import PostForm,Commentform
from django.views.generic import (TemplateView,ListView,
                DetailView,UpdateView,CreateView,
                DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog/about_us.html'

    
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostListView(ListView):
    model = Post
    #template_name = 'blog/post_list.html'
    # context_object_name = 'post_list'
    def get_queryset(self):
         return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #queryset = Post.objects.all()
    # model = Post
    # queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # template_name = 'blog/post_list.html'
    # context_object_name = 'posts'

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context
    
class PostDetailView(DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = "accounts/login"
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')













#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = Commentform(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = Commentform()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)


