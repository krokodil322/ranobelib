import json

from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse

from .models import Chapter, Work


# ================================ РЕДАКТОР ГЛАВ ПРОИЗВЕДЕНИЙ MARKDOWN  ================================

"""
    Пара editor и save_chapter - это функции отвечающие за запуск markdown редактора
    и сохранения глав из него в БД.
    
    Обе эти функции работают в 2-ух режимах: 1) Режим создания главы. 2) Режим редактирования главы.
    При пуше из 1-го режима создается новая глава в БД. При пуше из 2-го режима обновляется уже
    существующая глава. Обе эти функции защищены и доступны только для админов и staff'ов.
"""


@staff_member_required
def editor(request, slug: str, chapter_id: int | None=None) -> HttpResponse:
    """
    Открывает markdown редактор в одном из режиме:
        1) Создать новую главу.
        2) Редактировать уже существующую.
    
    Какой режим запустится зависит от chapter_id:
        1) Если chapter_id is None - запустить 1-ый режим.
        2) Иначе, значит, что глава есть - запустить 2-ой режим.
        
    Про URL:
        1) Открыть пустой редактор:  GET  /editor/<slug>/new/          
        2) Редактировать главу:      GET  /editor/<slug>/<chapter_id>/ 
        
    slug - это слаг произведения для создания красивой URL ссылке.
        
    Вызвать данный метод может только админ или staff благодаря декоратору @staff_member_required.
    """

    # объект главы
    chapter: Chapter | None = None
    
    # если глава есть, запускаем режим редактирования
    if chapter_id is not None:
        # получаем главу по chapter_id, если ее нет в БД django выдаст ошибку 404
        # если chapter по pk=chapter_id нет в БД, то Django автоматом вернет 404.
        # тут особый поиск, его суть: Найди главы с chapter_id, но только если эта глава
        # действительно принадлежит произведению с таким slug.
        chapter: Chapter = get_object_or_404(
            Chapter.objects.select_related("work"), 
            pk=chapter_id,
            work__slug=slug
        )
        work: Work = chapter.work
    else:
        # объект произведения
        work: Work = get_object_or_404(Work, slug=slug)

    # крафтим обратную ссылку в админку из редактора
    # данный вариант крафта хорош тем, что, если название приложения поменяется
    # то данная ссылка не полетит к чертям
    admin_back_url = reverse("admin:library_work_change", args=[work.pk])
    
    # перенаправляем в markdown editor
    # если chapter None, выставляем флаг is_new_mode в True режим, что
    # значит, запустится 1-ый режим. Если chapter все таки есть, то
    # запускаем во 2-ом режиме.
    print(f"IS NEW: {chapter is None}")
    return render(
        request, "editor.html", 
        {
            "chapter": chapter,
            "admin_back_url": admin_back_url,
            "work": work,
            "is_new_mode": chapter is None
        })


@staff_member_required
@require_POST
def save_chapter(request, slug: str, chapter_id: int | None=None) -> JsonResponse:
    """
    Данная функция является POST частью функции editor.
    Задача этой функции запушить главу в БД в 2-ух возможных режимах:
        1) Создать новую главу, если ее не существует.
        2) Обновить уже существующую.
    
    Режим зависит от того, какой chapter_id придет, если None,
    то режим создания новой главы, иначе обновление уже существующей.
    
    slug - это слаг произведения для создания красивой URL ссылке.

    Связанные URL c данной функцией:
        1) Создать главу в БД:  POST /save_chapter/<slug>/new/          
        2) Обновить главу в БД:      POST /save_chapter/<slug>/<chapter_id> 
   
    Сохраняет текст главы произведения из редактора текста
    в БД по id главы(chapter_id) прямо в формате markdown.
    
    Вызвать данный метод может только админ или staff благодаря декоратору @staff_member_required.
    Срабатывает только от POST метода благодаря декоратору @require_POST.
    """
    
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
    title: str = content_from_editor.get("title", "")
    # если название не указано возвращаем сообщение об ошибки
    if not title:
        return JsonResponse({"ok": False, "error": "Не указано название главы"}, status=400)
    
    # если режим редактирования главы
    if chapter_id is not None:
        # если chapter по pk=chapter_id нет в БД, то Django автоматом вернет 404.
        # тут особый поиск, его суть: Найди главы с chapter_id, но только если эта глава
        # действительно принадлежит произведению с таким slug.
        chapter: Chapter = get_object_or_404(
            Chapter, 
            pk=chapter_id,
            work__slug=slug
        )
    
        # подставляем новый контент и название в сущность главы и сохраняем в бд
        chapter.content = content
        chapter.title = title
        chapter.save(update_fields=["title", "content", "updated_at"])
    # если режим создания главы
    else:
        work = get_object_or_404(Work, slug=slug)
        chapter = Chapter.objects.create(
            work=work,
            title=title,
            content=content
        )
        
    # отправляем сообщение админу об успешном сохранении
    return JsonResponse({"ok": True, "message": "Глава сохранена в БД", "chapter_id": chapter.pk})


# ======================================================================================================



