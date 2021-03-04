from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .generatereport import PDFReport

from .models import Recipe, Ingredient, IngredientAmount
from .forms import RecipeForm
from .utils import get_ingredients, create_paginator
from .utils import (
    get_data_recipes_list,
    get_form_tags_with_status,
    _is_valid_input_data,
)

User = get_user_model()


def index(request):
    data = get_data_recipes_list(
        request=request,
        recipes=Recipe.objects.all(),
        title="Рецепты",
    )
    return render(request, "index.html", data)


def recipe_view(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(request, "singlePage.html", {"recipe": recipe})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    data = get_data_recipes_list(
        request=request,
        recipes=author.recipes.all(),
        title=author.username,
    )
    data["author"] = author
    return render(request, "authorRecipe.html", data)


@login_required
def follow_index(request):
    authors = User.objects.filter(followed_by__user=request.user).order_by("id")
    paginator, page = create_paginator(request, authors)
    return render(request, "myFollow.html", {"page": page, "paginator": paginator})


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients = get_ingredients(request.POST)

    if not _is_valid_input_data(form, ingredients):
        tags = get_form_tags_with_status(form)
        return render(
            request,
            "formRecipe.html",
            {
                "form": form,
                "tags": tags,
            },
        )

    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    for ingredient_name, ingredient_quantity in ingredients.items():
        ingredient_obj = get_object_or_404(Ingredient, name=ingredient_name)
        ingredient_amount = IngredientAmount(
            recipe=recipe, ingredient=ingredient_obj, quantity=ingredient_quantity
        )
        ingredient_amount.save()
    form.save_m2m()
    return redirect("main_page")


@login_required
def edit_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.user != recipe.author and not request.user.is_superuser:
        return redirect("main_page")

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    ingredients = get_ingredients(request.POST)

    if not _is_valid_input_data(form, ingredients):
        tags = get_form_tags_with_status(form)
        ingredients_for_render = IngredientAmount.objects.filter(recipe=recipe)
        return render(
            request,
            "formChangeRecipe.html",
            {
                "form": form,
                "tags": tags,
                "ingredients": ingredients_for_render,
                "recipe_slug": recipe_slug,
            },
        )

    IngredientAmount.objects.filter(recipe=recipe).delete()
    recipe = form.save(commit=False)
    recipe.save()
    for ingredient_name, ingredient_quantity in ingredients.items():
        ingredient_obj = get_object_or_404(Ingredient, name=ingredient_name)
        ingredient_amount = IngredientAmount(
            recipe=recipe, ingredient=ingredient_obj, quantity=ingredient_quantity
        )
        ingredient_amount.save()
    form.save_m2m()
    return redirect("main_page")


@login_required
def delete_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.user != recipe.author:
        return redirect("main_page")
    recipe.delete()
    return redirect("main_page")


@login_required
def favorite(request):
    data = get_data_recipes_list(
        request=request,
        recipes=Recipe.objects.filter(favorited_by__user=request.user),
        title="Избранное",
    )
    return render(request, "favorite.html", data)


@login_required
def shoplist(request):
    recipes = Recipe.objects.filter(added_to_shoplist_by__user=request.user)
    return render(
        request,
        "shopList.html",
        {
            "recipes": recipes,
        },
    )


@login_required
def shoplist_download(request):
    ingredient_amount = IngredientAmount.objects.filter(
        recipe__added_to_shoplist_by__user=request.user
    )
    ingredients_for_draw = {}
    for ingredient in ingredient_amount:
        name = ingredient.ingredient.name
        unit = ingredient.ingredient.unit
        quantity = ingredient.quantity
        if name not in ingredients_for_draw:
            ingredients_for_draw[name] = {
                "unit": unit,
                "quantity": quantity,
            }
        else:
            ingredients_for_draw[name]["quantity"] += quantity

    report = PDFReport()
    report.draw_ingredients(ingredients_for_draw)
    response = report.close_and_save()

    return response


def page_not_found(request, exception):
    return render(request, "misc/404.html", status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
