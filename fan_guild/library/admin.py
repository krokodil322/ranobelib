from django.contrib import admin
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
    fields =  ("title", "content", "order_num")
    ordering = ("order_num",)
    
# ===========================================

# ================ CПРАВОЧНИКИ ================

class Admin(admin.ModelAdmin):
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
    
    # данный атрибут определяет какие колонки
    # модели Work будут показываться в админке.
    list_display = (
        "id",
        "title_ru",
        "title_orig",
        "description",
        "cover_path",
        "rating",
        "views_count",
        "likes_count",
        "favorites_count",
        "is_published",
        "created_at",
        "updated_at"
    )
    
    # опеределяет по каким полям работает поиск сверху
    search_fields = (
        "title_ru",
        "title_orig",
        "slug"
    )
    
    # поля фильтра который находится справа в админке
    list_filter = (
        "work_type",
        "status",
        "age_rating",
        "orig_lang",
        "is_published",
        "created_at",
        "updated_at"
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
        "themes"
    )
    
    # автозаполнение slug поля
    prepopulated_fields = {
        "slug": ("title_ru",)
    }
    
    # встраиваем модель Chapter внутрь модели
    # Work. О том зачем это нужно описано
    # В классе ChapterInline
    inlines = [ChapterInline]


@admin.register(Chapter)
class ChaptersAdmin(admin.ModelAdmin):
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






