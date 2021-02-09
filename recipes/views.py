from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Recipe, Tag, Ingredient, IngredientAmount
from .forms import RecipeForm


def get_ingredients(data):
    ingredients = {}
    for key, value in data.items():
        if 'nameIngredient' in key:
            ingredient_id = key.split('_')[1]
            ingredients[value] = int(data[f'valueIngredient_{ingredient_id}'])
    return ingredients


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
    data = request.POST
    if form.is_valid():
        print('ВОШЛИ')
        ingredients = get_ingredients(request.POST)
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        for ingredient_name, ingredient_quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, name=ingredient_name)
            print(f'{ingredient} xx||xx {ingredient_quantity}')
            ingredient_amount = IngredientAmount(
                recipe=Recipe.objects.all().first(),
                ingredient=ingredient,
                quantity=ingredient_quantity
            )
            ingredient_amount.save()
        form.save_m2m()
        return redirect('main_page')
    tags = Tag.objects.all()
    return render(request, "formRecipe.html", {
        "form": form,
        'tags': tags,
    })
