from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)

    def __str__(self):
            return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
            return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    description = models.TextField()
    ingredient = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        blank=True)
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes')
    time = models.DurationField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
            return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amounts'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='ingredient_amounts'
    )
    quantity = models.FloatField()

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def save(self, *args, **kwargs):
        print('Save method executed!')
        super(IngredientAmount, self).save(*args, **kwargs)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    class Meta:
        unique_together = ('user', 'author')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited'
    )

    class Meta:
        unique_together = ('user', 'recipe')
