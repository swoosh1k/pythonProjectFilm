from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *




class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label = 'Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'url')
    list_display_links = ('name',)



class ReviewInline(admin.StackedInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')



class MovieShortsInline(admin.StackedInline):
    model = MovieShorts
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f"<img scr = {obj.image.url} width = '50' height='60'")


    get_image.short_description = 'Кадр из фильма'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'get_poster', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('titlte', 'category__name')
    inlines = [MovieShortsInline,ReviewInline]
    save_on_top = True
    save_as = True
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    list_editable = ('draft',)

    def get_poster(self, obj):
        return mark_safe(f"<img scr = {obj.poster.url} width = '50'height = '60' ")


    get_poster.short_description = 'Изображение'

    def unpublish(self, request, queryset):
        '''Снять с публикации'''
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена '
        else:
            message_bit = f' {row_update} записей были  обновлены '
        self.message_user(request, f'{message_bit}')


    def publish(self, request, queryset):
        '''Опубликовать '''
        row_update = queryset.update(draft = False)
        if row_update == 1:
            message_bit = '1 запись была обновлена '
        else:
            message_bit = f'{row_update} записей было обновлено '
        self.message_user(request, f"{message_bit}")

    publish.short_description = 'Опубликовать'
    publish.allowed_permission = ('change', )

    unpublish.short_description = 'Снять с публикации '
    unpublish.allowed_permission = ('change', )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    lits_display = ('name','email','parent','movie','id')
    readonly_fields = ('name','email')






@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age','get_image' )
    list_filter = ('age',)

    def get_image(self, obj):
        return mark_safe(f'<img scr = {obj.image.url} width ="50" height="60"' )

    get_image.short_description = 'Изображение'

@admin.register(MovieShorts)
class MovieShortsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img scr = {obj.image.url } width ='50' height='60'")

    get_image.short_description = 'Картинка из фильма'





@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie', 'ip')



admin.site.register(RatingStar)
admin.site.register(Genre)




admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'


