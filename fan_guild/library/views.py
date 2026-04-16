import json

from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse

from .models import Chapter


# ================================ РЕДАКТОР ГЛАВ ПРОИЗВЕДЕНИЙ MARKDOWN  ================================

"""
    Пара editor и save_chapter - предназначена для редактирования уже существующих глав.
    С их помощью нельзя создать новую главу, ибо это невозможно архитектурно.
    Они напрямую привязаны к кнопкам Редактировать(в самой админке) и Сохранить в БД(В редакторе).
    
    Пара editor_new и create_chapter - предназначена для создания глав прямо из тектового редактора.
    Для любой главы эти 2 метода сработают лишь один раз для ее создания, если глава уже существует, кнопки,
    Создать не будет!
"""


@staff_member_required
def editor(request, slug: str, chapter_id: int) -> HttpResponse:
    """
        Открывает редактор главы произведения по id главы(chapter_id).
        
        Вызвать данный метод может только админ или staff 
        благодаря декоратору @staff_member_required.
        
        slug - это слаг произведения для создания красивой URL ссылке.
        В данную функцию его надо передавать, но пока он тут не нужен.
        
        Важное замечание: Данная функция срабатывает только для глав
        которые уже есть БД. То есть, данная функция привязана к кнопке Редактировать.
    """
    # получаем главу по chapter_id, если ее нет в БД django выдаст ошибку 404
    chapter: Chapter | Http404 = get_object_or_404(Chapter, pk=chapter_id)
    
    # крафтим обратную ссылку в админку из редактора
    # данный вариант крафта хорош тем, что, если название приложения поменяется
    # то данная ссылка не полетит к чертям
    admin_back_url = reverse("admin:library_work_change", args=[chapter.work.id])
    
    # перенаправляем в редактор
    return render(
        request, "editor.html", 
        {
            "chapter": chapter,
            "admin_back_url": admin_back_url,
        })


@staff_member_required
@require_POST
def save_chapter(request, slug: str, chapter_id: int) -> HttpResponse:
    """
        Сохраняет текст главы произведения из редактора текста
        в БД по id главы(chapter_id) прямо в формате markdown.
        
        Вызвать данный метод может только админ или staff 
        благодаря декоратору @staff_member_required.
        
        Срабатывает только от POST метода благодаря 
        декоратору @require_POST.
        
        slug - это слаг произведения для создания красивой URL ссылке.
        В данную функцию его надо передавать, но пока он тут не нужен.
        
        Важное замечание: Данная функция срабатывает только для глав
        которые уже есть БД. То есть, данная функция привязана к кнопке Редактировать.
    """
    # если chapter по pk=chapter_id нет в БД, то Django автоматом вернет 404.
    chapter: Chapter | Http404 = get_object_or_404(Chapter, pk=chapter_id)
    
    # читаем данные(текст главы) которые прилетели от фронтенда
    # Данные присылет нам JavaScript(editor.js) прямо из markdown редактора в request.
    try:
        # получаем данные из request из сереализуем в dict python.
        content_from_editor: dict = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        # если JavaScript прислал нам косяный JSON, то сообщаем о ней данным ответом.
        return JsonResponse({"ok": False, "error": "Некорректный JSON"}, status=400)

    # если админ оставил текстовое поле пустым, то мы просто подставляем пустую строку
    content: str = content_from_editor.get("content", '')
    # тут обязательно должно быть название главы
    title: str = content_from_editor.get("title")
    # если название не указано возвращаем сообщение об ошибки
    if not title:
        return JsonResponse({"ok": False, "error": "Не указано название главы"}, status=400)
    
    # подставляем новый контент и название в сущность главы и сохраняем в бд
    chapter.content = content
    chapter.title = title
    chapter.save(update_fields=["title", "content", "updated_at"])
    
    # отправляем сообщение админу об успешном сохранении
    return JsonResponse({"ok": True, "message": "Глава сохранена в БД", "chapter_id": chapter_id})
    

# ======================================================================================================



