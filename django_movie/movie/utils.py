from .models import *






class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        last_movies = Movie.objects.order_by('id')[:5]
        context['categories'] = categories
        context['last_movies'] = last_movies

        return context