from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Recipe, Tag


def create_paginator(request, recipes):
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return (paginator, page)


def index(request):
    if request.method == 'GET' and 'tag' in request.GET:
        recipes = Recipe.objects.filter(tag__slug=request.GET['tag'])
    else:
        recipes = Recipe.objects.all()
    tags = Tag.objects.all()
    paginator, page = create_paginator(request, recipes)
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        'tags': tags,
    })
