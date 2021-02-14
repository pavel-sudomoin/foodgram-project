from django.contrib import admin
from django.urls import include, path
#from django.contrib.flatpages import views
#from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

#handler404 = "posts.views.page_not_found"
#handler500 = "posts.views.server_error"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("", include("recipes.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('about/', include('about.urls', namespace='about')),
    #path("about/", include("django.contrib.flatpages.urls")),
    #path("about-author/", views.flatpage, {"url": "/about-author/"}, name="author"),
    #path("about-spec/", views.flatpage, {"url": "/about-spec/"}, name="spec"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
