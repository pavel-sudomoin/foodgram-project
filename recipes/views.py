from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

from .models import Recipe, Tag, Ingredient, IngredientAmount
from .forms import RecipeForm
from .utils import get_ingredients, create_paginator, get_data_recipes_list, get_form_tags_with_status


reportlab.rl_config.TTFSearchPath.append(
    str(settings.BASE_DIR + settings.STATIC_URL)
)


def index(request):
    data = get_data_recipes_list(
        request=request,
        recipes=Recipe.objects.all(),
        title='Рецепты',
    )
    return render(request, 'index.html', data)


def recipe_view(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(request, 'singlePage.html', {
        'recipe': recipe
    })


def profile(request, username):
    User = get_user_model()
    author = get_object_or_404(User, username=username)
    data = get_data_recipes_list(
        request=request,
        recipes=author.recipes.all(),
        title=author.username,
    )
    data['author'] = author
    return render(request, 'authorRecipe.html', data)


@login_required
def follow_index(request):
    User = get_user_model()
    authors = User.objects.filter(followed_by__user=request.user).order_by('id')
    paginator, page = create_paginator(request, authors)
    return render(request, 'myFollow.html', {
        'page': page,
        'paginator': paginator
    })


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        ingredients = get_ingredients(request.POST)
        if not ingredients:
            form.add_error(
                'ingredient',
                'Вы не добавили ни одного ингридиента'
            )
        else:
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for ingredient_name, ingredient_quantity in ingredients.items():
                ingredient_obj = get_object_or_404(Ingredient,
                                                   name=ingredient_name)
                ingredient_amount = IngredientAmount(
                    recipe=recipe,
                    ingredient=ingredient_obj,
                    quantity=ingredient_quantity
                )
                ingredient_amount.save()
            return redirect('main_page')
    tags = get_form_tags_with_status(form)
    return render(request, 'formRecipe.html', {
        'form': form,
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
        ingredients = get_ingredients(request.POST)
        if not ingredients:
            form.add_error(
                'ingredient',
                'Вы не добавили ни одного ингридиента'
            )
        else:
            IngredientAmount.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for ingredient_name, ingredient_quantity in ingredients.items():
                ingredient_obj = get_object_or_404(Ingredient,
                                                   name=ingredient_name)
                ingredient_amount = IngredientAmount(
                    recipe=recipe,
                    ingredient=ingredient_obj,
                    quantity=ingredient_quantity
                )
                ingredient_amount.save()
            return redirect('main_page')
    tags = get_form_tags_with_status(form)
    ingredients_for_render = IngredientAmount.objects.filter(recipe=recipe)
    return render(request, 'formChangeRecipe.html', {
        'form': form,
        'tags': tags,
        'ingredients': ingredients_for_render,
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
    data = get_data_recipes_list(
        request=request,
        recipes=Recipe.objects.filter(favorited_by__user=request.user),
        title='Избранное',
    )
    return render(request, 'favorite.html', data)


@login_required
def shoplist(request):
    recipes = Recipe.objects.filter(added_to_shoplist_by__user=request.user)
    return render(request, 'shopList.html', {
        'recipes': recipes,
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


def page_not_found(request, exception):
    return render(request, 'misc/404.html', status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
