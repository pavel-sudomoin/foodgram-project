from django.core.paginator import Paginator

from .models import Tag, Ingredient


def get_ingredients(data):
    ingredients = {}
    for key, value in data.items():
        if "nameIngredient" in key:
            ingredient_id = key.split("_")[1]
            ingredients[value] = data[f"valueIngredient_{ingredient_id}"]
    return ingredients


def create_paginator(request, recipes):
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return paginator, page


def get_tags_with_status(selected_tags):
    tags = []
    for tag in Tag.objects.all():
        href = selected_tags.copy()
        is_selected = False
        if tag.slug in href:
            href.remove(tag.slug)
            is_selected = True
        else:
            href.append(tag.slug)
        href = "&tag=".join(href)
        if href:
            href = f"?tag={href}"
        tags.append(
            {
                "name": tag.name,
                "slug": tag.slug,
                "color_class": f"tags__checkbox_style_{tag.color}",
                "is_selected": is_selected,
                "href": href,
            }
        )
    return tags


def get_data_recipes_list(request, recipes, title):
    selected_tags = []
    current_href = ""
    if request.method == "GET" and "tag" in request.GET:
        selected_tags = request.GET.getlist("tag")
        recipes = recipes.filter(tag__slug__in=selected_tags).distinct()
    if selected_tags:
        current_href = f'&tag={"&tag=".join(selected_tags)}'
    tags = get_tags_with_status(selected_tags)
    paginator, page = create_paginator(request, recipes)
    return {
        "page": page,
        "paginator": paginator,
        "tags": tags,
        "current_href": current_href,
        "title": title,
    }


def get_form_tags_with_status(form):
    tags = []
    for tag_field in form["tag"]:
        tag_model = Tag.objects.get(name=tag_field.data["label"])
        tags.append(
            {
                "name": tag_model.name,
                "id_for_label": f"id_{tag_model.slug}",
                "value": tag_field.data["value"],
                "selected": tag_field.data["selected"],
                "color": tag_model.color,
            }
        )
    return tags


def _is_valid_input_data(form, ingredients):
    if not form.is_valid():
        return False
    if not ingredients:
        form.add_error(None, "Вы не добавили ингредиентов")
        return False
    for ingredient_name, ingredient_quantity in ingredients.items():
        if not Ingredient.objects.filter(name=ingredient_name).exists():
            form.add_error(None, f"Ингридиент {ingredient_name} не найден в базе")
            return False
        try:
            ingredients[ingredient_name] = round(float(ingredient_quantity), 1)
        except ValueError:
            form.add_error(
                None, f"Неверно указано количество ингридиента {ingredient_name}"
            )
            return False
    return True
