from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.conf import settings

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

from .models import Recipe, Tag, Ingredient, IngredientAmount
from .forms import RecipeForm


reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR + settings.STATIC_URL))


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
    selected_tag = None
    if request.method == 'GET' and 'tag' in request.GET:
        selected_tag = request.GET['tag']
        recipes = Recipe.objects.filter(tag__slug=selected_tag)
    else:
        recipes = Recipe.objects.all()
    tags = Tag.objects.all()
    paginator, page = create_paginator(request, recipes)
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator,
        'tags': tags,
        'selected_tag': selected_tag,
    })


def recipe_view(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(request, "recipe.html", {
        "recipe": recipe
    })


def profile(request, username):
    User = get_user_model()
    author = get_object_or_404(User, username=username)
    selected_tag = None
    if request.method == 'GET' and 'tag' in request.GET:
        selected_tag = request.GET['tag']
        recipes =  author.recipes.filter(tag__slug=selected_tag)
    else:
        recipes = author.recipes.all()
    tags = Tag.objects.all()
    paginator, page = create_paginator(request, recipes)
    return render(request, "authorRecipe.html", {
        "page": page,
        "paginator": paginator,
        'tags': tags,
        'author': author,
        'selected_tag': selected_tag,
    })


@login_required
def follow_index(request):
    User = get_user_model()
    authors = User.objects.filter(followed_by__user=request.user)
    paginator, page = create_paginator(request, authors)
    return render(request, "follow.html", {
        "page": page,
        "paginator": paginator
    })


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        ingredients = get_ingredients(request.POST)
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        for ingredient_name, ingredient_quantity in ingredients.items():
            ingredient_obj = get_object_or_404(Ingredient, name=ingredient_name)
            ingredient_amount = IngredientAmount(
                recipe=recipe,
                ingredient=ingredient_obj,
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


@login_required
def edit_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.user != recipe.author:
        return redirect('main_page')
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        IngredientAmount.objects.filter(recipe=recipe).delete()
        ingredients = get_ingredients(request.POST)
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        for ingredient_name, ingredient_quantity in ingredients.items():
            ingredient_obj = get_object_or_404(Ingredient, name=ingredient_name)
            ingredient_amount = IngredientAmount(
                recipe=recipe,
                ingredient=ingredient_obj,
                quantity=ingredient_quantity
            )
            ingredient_amount.save()
        form.save_m2m()
        return redirect('main_page')

    tags = []
    for tag_field in form['tag']:
        tag_model = Tag.objects.get(name=tag_field.data['label'])
        tags.append({
            'name': tag_model.name,
            'id_for_label': f'id_{tag_model.slug}',
            'value': tag_field.data['value'],
            'selected': tag_field.data['selected'],
            'color': tag_model.color
        })

    ingredient_amount_for_render = IngredientAmount.objects.filter(recipe=recipe)

    return render(request, "formChangeRecipe.html", {
        "form": form,
        'tags': tags,
        'ingredients': ingredient_amount_for_render,
        'recipe_slug': recipe_slug,
    })


@login_required
def delete_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.user != recipe.author:
        return redirect('main_page')
    recipe.delete()
    return redirect('main_page')


@login_required
def favorite(request):
    recipes = Recipe.objects.filter(favorited_by__user=request.user)
    selected_tag = None
    if request.method == 'GET' and 'tag' in request.GET:
        selected_tag = request.GET['tag']
        recipes = recipes.filter(tag__slug=selected_tag)
    paginator, page = create_paginator(request, recipes)
    tags = Tag.objects.all()
    return render(request, "favorite.html", {
        "page": page,
        "paginator": paginator,
        'tags': tags,
        'selected_tag': selected_tag,
    })


@login_required
def shoplist(request):
    recipes = Recipe.objects.filter(added_to_shoplist_by__user=request.user)
    return render(request, "shopList.html", {
        "recipes": recipes,
    })


@login_required
def shoplist_download(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ingredients.pdf"'

    ingredient_amount = IngredientAmount.objects.filter(
        recipe__added_to_shoplist_by__user=request.user
    )
    ingredients_for_output = {}
    for ingredient in ingredient_amount:
        name = ingredient.ingredient.name
        unit = ingredient.ingredient.unit
        quantity = ingredient.quantity
        if name not in ingredients_for_output:
            ingredients_for_output[name] = {
                'unit': unit,
                'quantity': quantity,
            }
        else:
            ingredients_for_output[name]['quantity'] += quantity

    c = canvas.Canvas(response)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    c.setFont('FreeSans', 14)
    textobject = c.beginText(2*cm, 29.7*cm - 2*cm)
    for name, data in ingredients_for_output.items():
        textobject.textLine(f"{name} ({data['unit']}) — {data['quantity']}")
    c.drawText(textobject)
    c.showPage()
    c.save()

    return response
