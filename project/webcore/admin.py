
from django.contrib import admin, messages
from django.db.models import Count
from .models import *
from decimal import Decimal


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}



class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author', 'text', 'is_approved')
    show_change_link = True

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title','rubric','price','is_published','created_at','seller','comment_count')
    list_display_links = ('title',)
    list_editable = ('is_published','price')
    list_per_page = 10
    date_hierarchy = 'created_at'

    search_fields = ('title','content','rubric__name', 'seller__username')
    ordering = ('-created_at',)
    list_filter = ('rubric', 'is_published', 'created_at')

    list_select_related = ('rubric', 'seller')

    fields = (('title', 'slug'),'rubric','seller','price','is_published','content',('created_at', 'updated_at'))
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (CommentInline,)

    def get_queryset(self, request):
        qs= super().get_queryset(request).annotate(c_count=Count('comments'))
        return qs

    @admin.display(ordering='c_count', description='Количество комментариев')
    def comment_count(self, obj):
        return obj.c_count

    @admin.action(description='Опубликовать объявления')
    def publish(self, request, queryset):
        updated=queryset.update(is_published=True)
        self.message_user(request,f"Опубликовано {updated} объявлений",messages.SUCCESS)

    @admin.action(description='Снять объявления')
    def unpublish(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"Снято {updated} объявлений", messages.SUCCESS)

    @admin.action(description='Сделать скидку 10 процентов')
    def discount_10(self,request,queryset):
        changed=0
        for ad in queryset:
            ad.price=(ad.price*Decimal('0.9')).quantize(Decimal('0.01'))
            ad.save(update_fields=['price'])
            changed+=1
        self.message_user(request,f"Скидка применена на {changed} объявлений",messages.SUCCESS)

    actions = [discount_10,publish,unpublish]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ad','author', 'text', 'is_approved','created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('ad__title','text')
    list_select_related = ('ad','author')
    readonly_fields = ('created_at',)




