from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import *
from django.urls import reverse, reverse_lazy
from django.views import View

from .form import *
from .models import Film


def get_all_films(request):
    all_films = Film.objects.all()
    context = {'all_films': all_films}
    template=get_template('films/films.html')
    return HttpResponse(template.render(context, request))

    # return render(request,'films/films.html',context)


def get_film_by_slug(request,slug):
    try:
        film = Film.objects.get(slug=slug)
        context = {'film': film}
    except Film.DoesNotExist:
        # return HttpResponse(status=404)
        raise Http404("Film does not exist")

        # return HttpResponseNotFound("Такое объявление не надйено")
    return render(request, 'films/film.html', context)


def get_film_by_id(request,pk):
    film = Film.objects.get(pk=pk)
    context = {'film': film}
    return render(request,'films/film.html',context)

def regular_films(request):
    all_films = Film.objects.all()
    context = {'all_films': all_films}
    return render(request,'films/films.html',context)

def add_film(request):
    filmform=FilmForm()
    context = {'form': filmform}
    return render(request,'films/add_film.html',context)


def add_saved_film(request):
    filmform=FilmForm(request.POST)
    if filmform.is_valid():
        filmform.save()
        return HttpResponseRedirect(reverse("films:all"))
    else:
        context = {'form': filmform}
        return render(request,'films/add_film.html',context)


def add_and_save_film(request):
    if request.method == "POST":
        filmform=FilmForm(request.POST)
        if filmform.is_valid():
            filmform.save()
            # return HttpResponseRedirect(f"http://127.0.0.1:8000/films/slug/{filmform.cleaned_data['slug']}/")
            return HttpResponseRedirect(reverse("films:film-by-slug",kwargs={"slug":filmform.cleaned_data['slug']}))
        else:
            context = {'form': filmform}
            return render(request, 'films/add_film.html', context)
    else:
        filmform = FilmForm()
        context = {'form': filmform}
        return render(request, 'films/add_film.html', context)


def index(request):
    response = HttpResponse("Здесь будет",content_type="text/plain; charset=utf-8")
    response.write(' главная')
    response.writelines((' страница ','сайта'))
    response["keywords"]="Python Django"
    return response




from .form import *
def film_create(request,method="factory"):
    FORM_MAP={
        "factory": FilmFormFactory,
        "quick": FilmForm,
        "full": FilmFullForm
    }
    FormClass=FORM_MAP.get(method,FilmFormFactory)
    if request.method=="POST":
        # form=FormClass(request.POST, request.FILES or None)
        form=FormClass(request.POST)
        if form.is_valid():
            film=form.save(commit=False)
            print(film.slug)
            film.save()
            return HttpResponseRedirect(reverse("films:all"))
    else:
        form=FormClass()
    return render(request,"films/add_film.html",{"form":form})


def film_create_html(request,mode="quick"):
    if request.method=="POST":
        form=FilmFullForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("films:all"))
    else:
        form=FilmFullForm()
    template="films/add_film.html" if mode=="quick" else "films/add_film_full.html"
    return render(request,template,{"form":form})





