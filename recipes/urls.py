from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="main_page"),
    path("follow/", views.follow_index, name="follow_index"),
    path("favorite/", views.favorite, name="favorite"),
    path("new/", views.new_recipe, name="new_recipe"),
    path("recipe/<str:recipe_slug>/", views.recipe_view, name="recipe"),
    path("recipe/<str:recipe_slug>/edit/", views.edit_recipe, name="edit_recipe"),
    path("recipe/<str:recipe_slug>/delete/", views.delete_recipe, name="delete_recipe"),
    path("user/<str:username>/", views.profile, name="profile"),
    path("shoplist/", views.shoplist, name="shoplist"),
    path("shoplist/download", views.shoplist_download, name="shoplist_download"),
#    path("follow/", views.follow_index, name="follow_index"),
#    path("group/<slug:slug>/", views.group_posts, name="group_posts"),
#    path("new/", views.new_post, name="new_post"),
#    path("<str:username>/", views.profile, name="profile"),
#    path("<str:username>/<int:post_id>/", views.post_view, name="post"),
#    path(
#        "<str:username>/<int:post_id>/edit/",
#        views.post_edit,
#        name="post_edit"
#    ),
#    path(
#        "<str:username>/<int:post_id>/comment",
#        views.add_comment,
#        name="add_comment"
#    ),
#    path(
#        "<str:username>/follow/",
#        views.profile_follow,
#        name="profile_follow"
#    ),
#    path(
#        "<str:username>/unfollow/",
#        views.profile_unfollow,
#        name="profile_unfollow"
#    )
]
