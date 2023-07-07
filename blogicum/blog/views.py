from django.shortcuts import render, get_object_or_404
from blog.models import Category, Post
from django.utils import timezone

POSTS_ON_MAIN = 5


def index(request):
    post_list = Post.objects.select_related(
        'location', 'author', 'category').filter(
            is_published__exact=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
    )[:POSTS_ON_MAIN]
    context = {
        'post_list': post_list
    }
    template_name = 'blog/index.html'
    return render(request, template_name, context)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post.objects.select_related(
        'location', 'author', 'category').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
    ), id=id)

    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )

    post_list = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        is_published__exact=True,
        category__is_published__exact=True,
        pub_date__lt=timezone.now(),
        category=category
    )

    context = {'category': category, 'post_list': post_list}

    return render(request, template_name, context)
