from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from .forms import ReviewForm, RatingForm
from .models import *
from .utils import DataMixin





class GenreYear:
    def get_genres(self):
        return Genre.objects.all()
    def get_years(self):
        return Movie.objects.filter(draft = False)


class MoviesView(GenreYear, ListView, DataMixin):
    paginate_by = 1
    model = Movie
    queryset = Movie.objects.filter(draft = False)
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        return dict(list(context.items()) + list(c_def.items()))



class MovieDetailView( DetailView, DataMixin):
    model = Movie
    slug_url_kwarg = 'film_slug'
    slug_field = 'url'
    template_name = 'movies/movie_detail.html'


    def get_context_data(self,*, object_list = None,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm
        c_def = self.get_user_context(title = Movie.title)
        return dict(list(context.items()) + list(c_def.items()))




class ActorDetail( DetailView, DataMixin):
    model = Actor
    slug_field = 'name'
    template_name = 'movies/actor.html'


    def get_context_data(self,*, object_list = None,  **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(tilte = Actor.name)
        return dict(list(context.items()) + list(c_def.items()))








class AddReview(View):
    '''Отзывы'''
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent.id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())



class FilterMovies(ListView,GenreYear, DataMixin):
    paginate_by = 1
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    model = Movie


    def get_queryset(self):
        return Movie.objects.filter(Q(year__in=self.request.GET.getlist('year')) | Q(genres__in = self.request.GET.getlist("genre"))).distinct()



class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(ip = self.get_client_ip(request), movie_id = int(request.POST.get('movie')), defaults={'star_id': int(request.POST.get('star'))})
            return  HttpResponse(status=201)
        else:
            return HttpResponse(status = 400)


class Search(GenreYear, DataMixin, ListView):
    template_name = 'movies/movie_list.html'
    model = Movie
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))


