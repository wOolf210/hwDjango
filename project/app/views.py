from django.contrib import messages
from django.core.paginator import Paginator
from django.http import *
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import *
from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin
from .mixins import RubricMixin, JsonResponseMixin, SuccessMessageMixin, RandomQuoteMixin, CurrentTimeMixin, \
    ResponseTimeHeaderMixin
from .models import *
from .form import *

from django.views.decorators.cache import cache_page, cache_control, never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers,vary_on_cookie

def index(request):
    s="Список объявлений\n\n\n\n\n"
    for b in Bb.objects.all():
        s += b.title + "\n"+ b.content+"\n\n\n"
    return HttpResponse(s,content_type="text/plain; charset=utf-8")

# @cache_page(60*5) # со стороны сервера
@vary_on_headers('User-Agent')# со стороны клиента
@cache_control(public=True, max_age=60*5) # со стороны клиента
def index_html(request):
    bbs=Bb.objects.all()
    rubrics=Rubric.objects.all()
    context={"bbs":bbs,"rubrics":rubrics}
    return render(request,'index.html',context)

@never_cache
def index2(request):
    return HttpResponse("Python Django")

def detail(request,pk):
    rubric=Rubric.objects.get(pk=pk)
    all_bb=Bb.objects.filter(rubric=rubric)
    context={"rubric":rubric,"all_bb":all_bb}
    return render(request,'detail.html',context)

def detail_bb(request,pk):
    bb=Bb.objects.get(pk=pk)
    context={"bb":bb}
    return render(request,'detail_bb.html',context)


def add_bb(request):
    if request.method=="POST":
        bbform=BbForm(request.POST)
        if bbform.is_valid():
            bbform.save()
            return HttpResponseRedirect(
                reverse
                ("app:detail",
                 kwargs={"pk":bbform.cleaned_data["rubric"].pk}
                 ))
        else:
            context={"form":bbform}
            return render(request,'add_bb.html',context)
    else:
        bbform=BbForm()
        context={"form":bbform}
        return render(request,'add_bb.html',context)

def stream(request):
    resp_content=('Здесь ','будет ','отправляться ','текст')
    return StreamingHttpResponse(
        resp_content,
        content_type="text/plain; charset=utf-8")

@require_GET
def file_response(request):
    file_path=r"C:\Users\winge\PycharmProjects\djangoProject1\project\static\picture.jpg"
    return FileResponse(open(file_path, 'rb'), content_type='image/jpg',as_attachment=True)

def our_decorator(func):
    def wrapper(request):
        print("hello")
        return func(request)
    return wrapper

@our_decorator
@require_http_methods(['POST'])
def json_response(request):
    bb=Bb.objects.get(title="Машина")
    dictionary={
        "title":bb.title,
        "content":bb.content,
        "price":bb.price,
        "published":bb.published,
    }
    return JsonResponse(dictionary)


def update_bb(request,pk):
    bb=Bb.objects.get(pk=pk)
    if request.method=="POST":
        form=BbForm(request.POST,instance=bb)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse
                ("app:detail",
                 kwargs={"pk": form.cleaned_data["rubric"].pk}
                 ))
        else:
            context = {"form": form}
            return render(request, 'add_bb.html', context)
    else:
        form = BbForm(instance=bb)
        context = {"form": form}
        return render(request, 'add_bb.html', context)

def delete_bb(request,pk):
    bb=get_object_or_404(Bb,pk=pk)
    if request.method=="POST":
        bb.delete()
        return redirect(reverse("app:index_html"))
    return Http404()



from django.views.generic import *
from django.views.generic.base import *
from django.contrib.auth.mixins import LoginRequiredMixin

class BbCreateView(SuccessMessageMixin,CreateView):
    model = Bb
    fields = ['rubric','title','content','price']
    template_name = "add_bb.html"
    success_message = "Объявление успешно создано"



class BbByRubricTemplateView(TemplateView):
    template_name = "by_rubric_class.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['bbs']=Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics']=Rubric.objects.all()
        context['current_rubric']=Rubric.objects.get(pk=context['rubric_id'])
        return context

from django.views import View
class RubricDetailView(View):
    def get(self, request, rubric_id):
        current_rubric=get_object_or_404(Rubric,pk=rubric_id)
        bbs=Bb.objects.filter(rubric=current_rubric)
        rubrics=Rubric.objects.all()
        context={
            "current_rubric":current_rubric,
            "bbs":bbs,
            "rubrics":rubrics,
        }
        return render(request,'by_rubric_class.html',context)

class BbDetailView(DetailView):
    model = Bb
    template_name = "detail_bb.html"
    # pk_url_kwarg = "bb_id"

@method_decorator(cache_page(60*5), name='dispatch')
class BbListView(ResponseTimeHeaderMixin,CurrentTimeMixin,RandomQuoteMixin, RubricMixin,ListView):
    model = Bb
    template_name = "index.html"
    context_object_name = "bbs"
    # allow_empty = False

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['rubrics']=Rubric.objects.all()
        data = ["Test1", "Test2", "Test3"]
        context["data"]= data
        return context


class BbJsonView(JsonResponseMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        bb=Bb.objects.first()
        data={
            "title": bb.title,
            "content": bb.content,
            "price": bb.price,
        }
        return self.render_to_json_response(data)


class BbUpdateView(UpdateView):
    # form_class = BbForm
    model = Bb
    fields = ['rubric','title','content','price']
    success_url = "app/all/class/"
    template_name = "add_bb.html"


class BbDeleteView(DeleteView):
    model = Bb
    success_url = reverse_lazy("app:all_class")
    template_name = "delete_bb.html"
    context_object_name = "bb"


class BbIndexArchiveView(ArchiveIndexView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"

class BbYearArchiveView(YearArchiveView):
    model = Bb
    template_name = "date.html"
    context_object_name = "latest"
    date_field = "published"
    make_object_list = True

class BbMonthArchiveView(MonthArchiveView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"
    make_object_list = True
    month_format = "%m"

class BbWeekArchiveView(WeekArchiveView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"
    make_object_list = True
    weekday_format = "%W"

class BbDayArchiveView(DayArchiveView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"
    make_object_list = True
    month_format = "%m"

class BbTodayArchiveView(TodayArchiveView):
    model = Bb
    date_field = "published"
    template_name = "date.html"
    context_object_name = "latest"
    make_object_list = True

class BbRedirectView(RedirectView):
    url = reverse_lazy("app:all_class")
    permanent = True


class MergeBbRubricView(SingleObjectMixin, ListView):
    template_name = "by_rubric_class.html"
    pk_url_kwarg = "rubric_id"

    def get(self, request,*args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['rubrics']=Rubric.objects.all()
        context['current_rubric']=self.object
        context['bbs']=context['object_list']
        return context

    def get_queryset(self):
        return self.object.bb_set.all()


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = "contact.html"
    success_url = reverse_lazy("app:all_class")

    def form_valid(self, form):
        print("Полученный данные",form.cleaned_data)
        return super().form_valid(form)


class TemplateAllBboard(ListView):
    model = Bb
    template_name = "all_bboard.html"
    context_object_name = "bbs"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['email']="test@gmail.com"
        context['phone']=""
        context['html_code']="<i>Hello</i>"
        return context


class TestView(TemplateView):
    template_name = "test.html"


class BootstrapFormView(FormView):
    form_class = ContactForm
    template_name = "bootstrap.html"
    success_url = reverse_lazy("app:all_class")

    def form_valid(self, form):
        print("Полученный данные",form.cleaned_data)
        return super().form_valid(form)



from django.core.paginator import Paginator

def bb_paginator(request):
    bbs = Bb.objects.all().order_by('-published')
    per_page = request.GET.get('per_page', 3)
    paginator = Paginator(bbs, per_page,orphans=2)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'bb_paginator.html', context)

from django.views.generic import ListView
from .models import Bb
from .paginators import NegativeLabelPaginator

class BbListViewPaginator(ListView):
    model = Bb
    template_name = "bb_paginator_custom.html"
    context_object_name = "bbs"
    paginate_by = 3
    paginator_class = NegativeLabelPaginator

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get("per_page")
        return int(per_page) if per_page and per_page.isdigit() else self.paginate_by

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        paginator  = ctx["paginator"]
        page_obj   = ctx["page_obj"]
        ctx["neg_page_range"] = paginator.get_negative_page_range()
        return ctx



class RubricSetView(View):
    template_name = "rubric_formset.html"

    def _get_formset(self, *, data=None):

        RubricFormSet = modelformset_factory(
            Rubric,
            fields=("name",),
            can_delete=True,
            extra=2,
            formset=RubricBaseFormSet,
        )
        return RubricFormSet(data=data, queryset=Rubric.objects.all())

    def get(self, request):
        formset = self._get_formset()
        return render(request, self.template_name, {"formset": formset})

    def post(self, request):
        formset = self._get_formset(data=request.POST)

        if formset.is_valid():
            formset.save()
            return redirect(reverse("app:all_class"))

        return render(request, self.template_name, {"formset": formset})

class QuizFormsetView(View):
    template_name = "quiz_formset.html"

    def get(self,request,pk):
        quiz=get_object_or_404(Quiz,pk=pk)
        formset=QuestionFormSet(instance=quiz)
        context={"formset":formset,"quiz":quiz}
        return render(request,self.template_name,context)

    def post(self,request,pk):
        quiz=get_object_or_404(Quiz,pk=pk)
        formset=QuestionFormSet(request.POST,instance=quiz)

        if formset.is_valid():
            formset.save()
            return redirect(reverse("app:quiz_formset", args=(quiz.pk,)))

        context={"formset":formset,"quiz":quiz}
        return render(request,self.template_name,context)

# DRY - Don't Repeat Yourself
# KISS - Keep It Simple, Stupid
# YAGNI - You Aren't Gonna Need It

from django.db import transaction
def manual_transaction_example(request):
    transaction.set_autocommit(False)
    sid=transaction.savepoint()
    try:
        rubric=Rubric.objects.create(name="Тестовая рубрика")
        Bb.objects.create(
            rubric=rubric,
            title="Тестовое объявление",
            content="Тестовое содержание",
            price=10000.0)
        Bb.objects.create(
            rubric=rubric,
            title="Тестовое объявление2",
            content="Тестовое содержание2",
            price=100.0)
        transaction.savepoint_commit(sid)
        transaction.commit()

    except Exception as e:
        transaction.savepoint_rollback(sid)
        transaction.rollback()
        transaction.set_autocommit(True)
        return HttpResponse(f"Произошла ошибка: {e}", status=500)
    finally:
        transaction.set_autocommit(True)
    return HttpResponse("Транзакция успешно выполнена", status=200)

# @transaction.non_atomic_requests
@transaction.atomic
def atomic_transaction_example(request):
    rubric=Rubric.objects.create(name="Атомарная рубрика")
    Bb.objects.create(
        rubric=rubric,
        title="Атомарное объявление",
        content="Атомарное содержание",
        price=199.0
    )
    transaction.on_commit(lambda: print("Транзакция успешно завершена"))
    return HttpResponse("Successed", status=200)


from django.core.cache import caches,cache
def cache_backend(request):
    db_cache=caches['db']
    added=db_cache.add("unique","value",timeout=None)
    counter=db_cache.get_or_set("counter",lambda:0,timeout=600)
    db_cache.incr("counter")
    cache.delete_many(["heavy_data","counter"])
    return HttpResponse(f"Count = {db_cache.get("counter")}")


def filter(request):
    return render(request, "filter.html")






from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .form import DocumentForm, PhotoForm, ManyDocsForm
from .models import Document, Photo

# Список документов
def docs_list(request):
    docs = Document.objects.order_by("-uploaded_at")
    return render(request, "files/docs_list.html", {"docs": docs})

# Загрузка одного документа (модельная форма)
class UploadDocumentView(View):
    def get(self, request):
        return render(request, "files/upload_doc.html", {"form": DocumentForm()})

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)  # важно: request.FILES
        if form.is_valid():
            form.save()
            return redirect("app:docs_list")
        return render(request, "files/upload_doc.html", {"form": form})

# Загрузка нескольких документов (не-модельная форма)
class UploadManyDocsView(View):
    def get(self, request):
        return render(request, "files/upload_many.html", {"form": ManyDocsForm()})

    def post(self, request):
        form = ManyDocsForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist("files"):  # забираем ВСЕ файлы
                Document.objects.create(file=f)
            return redirect("app:docs_list")
        return render(request, "files/upload_many.html", {"form": form})

def delete_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    storage = doc.file.storage
    name = doc.file.name
    doc.delete()
    if name:
        storage.delete(name)
    messages.success(request, "Документ успешно удален")
    return redirect("app:docs_list")

# Список фото
def photos_list(request):
    photos = Photo.objects.order_by("-created_at")
    return render(request, "files/photos_list.html", {"photos": photos})

# Загрузка фото (модельная форма)
class UploadPhotoView(View):
    def get(self, request):
        return render(request, "files/upload_photo.html", {"form": PhotoForm()})

    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("app:photos_list")
        return render(request, "files/upload_photo.html", {"form": form})

# Удаление фото — в самом моделe.delete() мы уже удаляем файл; вызовем просто .delete()
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect("app:photos_list")

def gallery_list(request):
    photos = PhotoResized.objects.order_by("-created_at")
    return render(request, "files/gallery_list.html", {"photos": photos})

from .form import PhotoResizedForm
from .models import PhotoResized

class UploadResizedPhotoView(View):
    def get(self, request):
        return render(request, "files/upload_resized.html", {"form": PhotoResizedForm()})
    def post(self, request):
        form = PhotoResizedForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("app:gallery_list")
        return render(request, "files/upload_resized.html", {"form": form})