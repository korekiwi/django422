from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

from posts_dataset import dataset
from help_functions import python_slugify, python_slugify_list

CATEGORIES = [
    {"slug": "python", "name": "Python"},
    {"slug": "django", "name": "Django"},
    {"slug": "postgresql", "name": "PostgreSQL"},
    {"slug": "docker", "name": "Docker"},
    {"slug": "linux", "name": "Linux"},
]


def main(request):
    # catalog_categories_url = reverse("blog:categories")
    # catalog_tags_url = reverse("blog:tags")

    context = {
        "title": "Главная страница",
        "text": "Текст главной страницы",
        "user_status": "moderator",
    }
    return render(request, "main.html", context)

def about(request):
    context = {
        "title": "О проекте",
        "project_information": "Информация о проекте",
        "contact": "Контактные данные",
    }

    return render(request, "about.html", context)


def catalog_posts(request):

    context = {
        "title": "Каталог постов",
        "dataset_posts": dataset,
    }
    
    return render(request, "catalog_posts.html", context)


def post_detail(request, post_slug):
    for post in dataset:
        if post.get('slug') == post_slug:
            context = post
            break

    return render(request, "post_detail.html", context)


def catalog_categories(request):
    # links = []
    # for category in CATEGORIES:
    #     url = reverse("blog:category_detail", args=[category["slug"]])
    #     links.append(f'<p><a href="{url}">{category["name"]}</a></p>')

    context = {
        "title": "Категории",
        "text": "Текст страницы с категориями",
        "categories": CATEGORIES,
    }
    return render(request, "catalog_categories.html", context)


def category_detail(request, category_slug):

    category = [cat for cat in CATEGORIES if cat["slug"] == category_slug][0]

    if category:
        name = category["name"]
    else:
        name = category_slug

    return HttpResponse(
        f"""
        <h1>Категория: {name}</h1>
        <p><a href="{reverse('blog:categories')}">Назад к категориям</a></p>
    """
    )


def catalog_tags(request):
    return HttpResponse("Каталог тегов")


def tag_detail(request, tag_slug):
    dataset_posts = []

    for post in dataset:
        if tag_slug in python_slugify_list(post.get('hashtags')):
            dataset_posts.append(post)

    context = {
        "title": f"Страница тега {tag_slug}",
        "slug": tag_slug,
        "dataset_posts": dataset_posts,
    }

    return render(request, "tag_detail.html", context)


    # return HttpResponse(f"Страница тега {tag_slug}")
