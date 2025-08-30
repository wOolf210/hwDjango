from django.core.validators import MinLengthValidator
from django.forms import *
from .models import *



class FilmFullForm(ModelForm):
    slug= SlugField(
        label="Уникальный идентификатор",
        help_text="Уникальный идентификатор фильма, используемый в URL",
        max_length=10,
        required=True,
        error_messages={
            "max_length":"Уникальный идентификатор не должен превышать 10 символов.",
        }
    )
    name=CharField(
        label="Название фильма",
        max_length=200,
        validators=[MinLengthValidator(2)],
        error_messages={
            "min_length": "Минимальная длина названия фильма - 2 символа.",
        }
    )

    author=CharField(
        label="Автор фильма",
        max_length=100,
    )
    genre=CharField(
        label="Жанр фильма",
        widget=TextInput(attrs={"size": 40, "placeholder": "Введите жанр фильма"}),
    )
    year=DateField(
        label="Год выпуска",
        widget=SelectDateWidget(years=range(1900, 2025)),
    )
    class Meta:
        model = Film
        fields = ['slug', 'name', 'genre', 'author', 'year']





class FilmForm(ModelForm):
    class Meta:
        model = Film
        fields = ['slug','name','genre','author','year']
        labels={
            "slug": "Уникальный идентификатор",
            "name": "Название фильма",
        }
        help_texts={
            "author": "Автор фильма",
        }
        widgets={
            "genre":TextInput(attrs={"size":40}),
            "year":SelectDateWidget(years=range(1900, 2025)),
        }


FilmFormFactory = modelform_factory(
    Film,
    fields="__all__",
    labels={
        "name": "Название",
        "year": "Год выпуска",
    },
    help_texts={
        "slug": "Уникальный идентификатор фильма, используемый в URL",
        "genre": "Жанр фильма, например: драма, комедия, боевик и т.д.",
    },
    widgets={
        "genre":TextInput(attrs={"placeholder": "Введите жанр фильма"}),
        "year":SelectDateWidget(years=range(1900, 2025)),
    }
)




