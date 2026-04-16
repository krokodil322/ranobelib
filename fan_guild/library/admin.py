from django import forms
from django.contrib import admin
from django.utils.timezone import localtime
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import SafeText
from .models import (
    Author,
    Translator,
    Fandom,
    Genre,
    Theme,
    WorkType,
    WorkStatuse,
    WorkOriginalLanguage,
    AgeRating,
    Work,
    Chapter
)
# Register your models here.


# ================ УДОБСТВО ================

class ChapterInline(admin.TabularInline):
    """
        Решает данную проблему:
            Добавлять новые главы по отдельности очень 
            не удобно, ибо нужно для каждой главы
            подставлять название произведения.
            
        Позволяет создавать и редактировать главы
        прямо внутри карточки произведения.
        Автоматически подставляет название произведения
        в новую главу.
    """
    model = Chapter
    extra = 1
    fields =  ("title", "content", "open_in_editor", "order_num")
    ordering = ("order_num",)
    readonly_fields = ("open_in_editor",)
    
    
    
    def open_in_editor(self, obj):
        """
            Добавляет кнопку редактировать для каждой главы произведения.
            Данная кнопка ведет в кастомный markdown редактор.
        """

        # тут не нужна проверка на наличие объекты в БД, ибо
        # новую главу можно создать прямо из редактора.
        if not obj.pk:
            return 'Создай перед редактированием'
        
        # если глава есть, то подставляем в нопку URL на markdown редактор.
        url = reverse("editor", kwargs={"slug": obj.work.slug, "chapter_id": obj.pk})
        return format_html(
            '<a class="button" href="{}" target="_blank">Редактировать</a>', 
            url
        )
    

class NoAutocompleteAdminForm(forms.ModelForm):
    """
        Данный класс фиксит автокомплит в комбобоксах.
        Штука в том, что бразуры хранят историю заполнения
        и начинают жестко гадить тем, чем не надо.
        
        Например: Когда хочешь добавить новый жанр,
        тыкаешь поле ввода жанра и снизу всплывает комобобокс,
        где много всяких данных, причем эти данные из других таблиц.
        Типо Ранобэ, Фанфик, R-17, и т. п.
        
        Зачем тебе эти подсказки когда ты просто добавляешь новый жанр?
        
        Чтобы фикс работал, нужно создать атрибут form для нужных классов:
            from = NoAutocompleteAdminForm
    """
    
    class Meta:
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "off"}),
        }

# ===========================================

# ================ CПРАВОЧНИКИ ================

class Admin(admin.ModelAdmin):   
    form = NoAutocompleteAdminForm 
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Author)
class AuthorsAdmin(Admin):
    pass


@admin.register(Translator)
class TranslatorsAdmin(Admin):
    pass


@admin.register(Fandom)
class FandomsAdmin(Admin):
    pass


@admin.register(Genre)
class GenresAdmin(Admin):
    pass    


@admin.register(Theme)
class ThemesAdmin(Admin):
    pass


@admin.register(WorkType)
class WorkTypesAdmin(Admin):
    pass


@admin.register(WorkStatuse)
class WorkStatusesAdmin(Admin):
    pass


@admin.register(WorkOriginalLanguage)
class WorkOriginalLanguagesAdmin(Admin):
    pass


@admin.register(AgeRating)
class AgeRatingsAdmin(Admin):
    pass

# =============================================


# ================ ГЛАВНЫЕ СУЩНОСТИ ================

@admin.register(Work)
class WorksAdmin(admin.ModelAdmin):
    """Регистрация и настройка модели Work в админке"""
    
    class Media:
        js = ('admin/form_persist.js',)
    
    # данный атрибут определяет какие колонки
    # модели Work будут показываться в админке.
    list_display = (
        "id",
        "title_ru",
        "title_orig",
        "short_description_admin",
        "cover_path",
        "rating",
        "views_count",
        "likes_count",
        "favorites_count",
        "is_published",
        "created_at_local_admin",
        "updated_at_local_admin",
        "published_at_local_admin"
    )
    
    # это поля по которым можно кликнуть чтобы начать редактировать произведение
    list_display_links = ("id", "title_ru")
    
    # поля которые нельзя редактировать
    readonly_fields = (
        "cover_preview",
        "created_at_local_admin",
        "updated_at_local_admin",
        "published_at_local_admin"
    )
    
    # отвечает за структуру и порядок редактора произведения
    fieldsets = (
        ("Основное", {
            "fields": (
                "title_ru",
                "title_orig",
                "description",
                "slug",
                "is_published",
            )
        }),
        ("Обложка", {
            "fields": (
                "cover_path",
                "cover_preview",
            )
        }),
        ("Классификация", {
            "fields": (
                "work_type",
                "status",
                "age_rating",
                "orig_lang",
                "authors",
                "genres",
                "themes",
                "translators",
                "fandoms",
            )
        }),
        ("Статистика", {
            "fields": (
                "rating",
                "views_count",
                "likes_count",
                "favorites_count",
            )
        }),
        ("Служебное", {
            "fields": (
                "created_at_local_admin",
                "updated_at_local_admin",
                "published_at_local_admin"
            )
        }),
    )
    
    # опеределяет по каким полям работает поиск сверху
    search_fields = (
        "title_ru",
        "title_orig",
        "slug",
    )
    
    # поля фильтра который находится справа в админке
    list_filter = (
        "work_type",
        "status",
        "age_rating",
        "orig_lang",
        "is_published",
        "created_at",
        "updated_at",
    )

    """
        Данный атрибут говорит Django о том, что для данных таблиц(только
        многие ко многим) покажи не обычный(неудобный) список, а более
        удобный интерфейс выбора. 
        
        Дефолтный интерфейс выглядит примерно так:
            Вываливаться комбобокс, где 1 строка - 1 жанр(например).
            Если ты хочешь выбрать несколько жанров, тебе  придется
            Зажимать CTRL и кликать мышкой, если значений много, это
            становится неудобно.
            
        С filter_horizontal Django покажет более удобный UI, где 
        покажется список из 2-ух колонок, где 1-ая колонка - это
        список жанров, а 2-ая колонка - это список жанров которые
        выбрал админ для данного произведения.
    """

    filter_horizontal = (
        "authors",
        "genres",
        "themes",
        "translators",
        "fandoms",
    )
    
    # автозаполнение slug поля
    prepopulated_fields = {
        "slug": ("title_ru",)
    }
    
    # встраиваем модель Chapter внутрь модели
    # Work. О том зачем это нужно описано
    # В классе ChapterInline
    inlines = [ChapterInline]
    
    @admin.display(description="Дата и время создания")
    def created_at_local_admin(self, obj):
        """Данный метод форматирует дату и время создания в привычный RU формат"""
        return obj.created_at_local()
    
    @admin.display(description="Дата и время изменения")
    def updated_at_local_admin(self, obj):
        """Данный метод форматирует дату и время изменения в привычный RU формат"""
        return obj.updated_at_local(obj)
    
    @admin.display(description="Дата и время публикации")
    def published_at_local_admin(self, obj):
        """Данный метод форматирует дату и время публикации произведения в привычный RU формат"""
        return obj.published_at_local()
    
    @admin.display(description="Описание")
    def short_description_admin(self, obj) -> str:
        """
            Данный метод сокращает описание произведения в админке.
            Это нужно, чтобы само описание жестко не спамилось в админке,
            ибо оно может занимать довольно много места.
        """
        return obj.short_description()
    
    @admin.display(description="Обложка")
    def cover_preview(self, obj) -> str | SafeText:
        """
            Данный метод нужен для превью обложки 
            произведения в админке. Чтобы в поле картинки
            стояла картинка, а не просто путь.
        """
        return obj.cover_preview()
    
    
@admin.register(Chapter)
class ChaptersAdmin(admin.ModelAdmin):
    """Регистрация и настройка глав в админке"""
    list_display = (
        "id",
        "work",
        "order_num",
        "title",
        "created_at",
        "updated_at"
    )
    
    """
        Тут интересный момент с work__title_ru.
        Он означает:
            из модели Chapter перейти в модель Work и
            взять поле title_ru из этой модели.
        
        Зачем это надо?
            Это позволяет искать главы по названию 
            произведения.
    """
    search_fields = (
        "title",
        "content",
        "work__title_ru",
    )

    list_filter = (
        "work",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("work",)
    ordering = ("work", "order_num")

# ==================================================






