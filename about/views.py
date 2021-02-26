from django.views.generic.base import TemplateView


class AboutProjectView(TemplateView):
    template_name = "project.html"


class AboutAuthorView(TemplateView):
    template_name = "author.html"


class AboutTechView(TemplateView):
    template_name = "tech.html"
