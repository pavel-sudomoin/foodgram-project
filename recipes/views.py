from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Recipe, Tag
from .forms import RecipeForm


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


def recipe_view(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(request, "recipe.html", {
        "recipe": recipe
    })


@login_required
def follow_index(request):
    User = get_user_model()
    authors = User.objects.filter(following__user=request.user)
    paginator, page = create_paginator(request, authors)
    return render(request, "follow.html", {
        "page": page,
        "paginator": paginator
    })


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save()
        recipe.author = request.user
        recipe.save()
        return redirect("index")
    tags = Tag.objects.all()
    return render(request, "formRecipe.html", {
        "form": form,
        'tags': tags,
    })