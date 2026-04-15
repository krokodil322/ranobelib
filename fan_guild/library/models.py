from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.safestring import SafeText
from django.utils.html import format_html

"""
Схема базы данных расписана в файле fan_guild_database_schema.drawio.

Хочу заметить, что в этой схеме таблиц больше, чем тут. Сразу объясняю
почему так:
    Штука в том, что Django сам создает вспомогательные таблицы, если
    эта вспомогательная таблица очень простая(как в нашем случае).
    
    Конкретно в этом коде, связывание genres, fandoms и т. п.
    происходит в таблице Works, где я четко отделил блок кода:
    СВЯЗИ МНОГИЕ КО МНОГИМ. Там специальный поля ManyToManyField,
    и там прописаны связи с соответствующими моделями.
    
    То есть, таблицы: work_themes, work_genres и т. п. создадутся
    автоматически.
    
    Этот вопрос было важно разобрать еще потому, что в этих таблицах
    явно есть constraint вида: UNIQUT (work_id, genre_id(или подобное)).
    То есть эти пары должны быть уникальными. Ибо зачем нужны дубли?
    Допустим произведение Re:Zero(work_id=10), имеет жанр: Fantasy(genre_id=3)
    Тогда в таблице work_genres будет такая запис:
    (works_id=10, genre_id=3). Дубль не нужен, ибо зачем на
    две записи Re:Zero с жанром Fantasy в таблице?
    Django сам прописывает данный constraint в таблице которую он тоже
    создает автоматичеки.
    
    Это обычная Django магия.
    
Во всех справочных таблицах название ключевого поля name. Это сделано
специально для упрощения и полиморфизма кода.

Это сильно упрощает код, ordering, __str__, админку и общее восприятие.    
"""


class Author(models.Model):
    """Это таблица справочная. В ней хранятся все авторы произведений"""
    
    # полное имя автора
    name = models.CharField("Полное имя автора", max_length=255, unique=True)

    class Meta:
        # имя таблицы в бд
        db_table = "authors"
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        
        # это настройка сортирует всех авторов в таблице по полю author в БД
        ordering = ["name"]
        
    def __str__(self) -> str:
        return self.name
    

class Translator(models.Model):
    """Это таблица справочная. В ней хранятся все авторы переводов"""
    
    # полное имя переводчика или команды перевода
    name = models.CharField(
        "Имя переводчика или команды", 
        max_length=255, 
        unique=True,
        help_text="AI, RanobeList, и т. п."
    )
    
    class Meta:
        db_table = "translators"
        verbose_name = "Переводчик"
        verbose_name_plural = "Переводчики"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name
    

class Fandom(models.Model):
    """Это таблица справочная. В ней хранятся все типы фандомов произведений"""
    
    # полное название фандома
    name = models.CharField(
        "Название фандома", 
        max_length=255, 
        unique=True,
        help_text="Наруто, Гарри Поттер, и т. п."
    )
    
    class Meta:
        db_table = "fandoms"
        verbose_name = "Фандом"
        verbose_name_plural = "Фандомы"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Это таблица справочная. В ней хранятся все типы жанров произведений"""
    
    # полное название жанра
    name = models.CharField(
        "Название жанра", 
        max_length=255, 
        unique=True,
        help_text="Фэнтези, Триллер, и т. п."
    )
    
    class Meta:
        db_table = "genres"
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]
        
    def __str__(self) -> str:
        return self.name


class Theme(models.Model):
    """Это таблица справочная. В ней хранятся все типы тем произведений"""
    
    # полное название темы
    name = models.CharField(
        "Название темы", 
        max_length=255, 
        unique=True,
        help_text="Исэкай, Историческая, и т. п."
    )
    
    class Meta:
        db_table = "themes"
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ["name"]
        
    def __str__(self) -> str:
        return self.name
    

class WorkType(models.Model):
    """
        Это таблица справочная. В ней хранятся  все типы произведений.
        Например: Ранобэ, фанфик, сянься, и т. п.
    """
    
    # полное название типа произведения
    name = models.CharField(
        "Название типа", 
        max_length=255, 
        unique=True,
        help_text="Ранобэ, фанфик, и т. п."
    )
    
    class Meta:
        db_table = "work_types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name


class WorkStatuse(models.Model):
    """
        Это таблица справочная. В ней хранятся все типы состояний произведения.
        Например: Вышло, выходит, анонс, и т. п.
    """
    
    # полное название статуса произведения
    name = models.CharField(
        "Название статуса", 
        max_length=255, 
        unique=True,
        help_text="Вышло, выходит, анонс, и т. п."
    )
    
    class Meta:
        db_table = "work_statuses"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name


class WorkOriginalLanguage(models.Model):
    """
        Это таблица справочная. В ней хранятся все языки оригиналов произведений.
        Например: Китайский, Японский, Корейский, и т. п.
    """
    name = models.CharField(
        "Язык оригинала", 
        max_length=255, 
        unique=True,
        help_text="Китайский, Японский, и т. п."
    )
    
    class Meta:
        db_table = "work_orig_langs"
        verbose_name = "Язык оригинала"
        verbose_name_plural = "Языки оригиналов"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name


class AgeRating(models.Model):
    """
        Это таблица справочная. В ней хранятся
        все виды возрастных рейтингов произведений.

        Например: G / PG-13 / R / NC-17

        У любого произведения может быть только
        один возрастной рейтинг.
    """
    # название возрастного рейтинга
    name = models.CharField(
        "Название возрастного рейтинга", 
        max_length=50, 
        unique=True,
        help_text="R-17, G, PG, PG-13, R, NC-17, и т. п."
    )

    class Meta:
        db_table = "age_ratings"
        verbose_name = "Возрастной рейтинг"
        verbose_name_plural = "Возрастные рейтинги"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Work(models.Model):
    """
        Таблица произведений. Этой схемой 
        описываются любые произведения на сайте. 

        Важно заметить, что сами главы любого 
        произведения не хранятся в этой таблице,
        а хранятся в таблице Chapters. В этой же
        таблице хранятся только метаданные
        (название, рейтинг, год выхода, статус, и т. п.).
    """
    
    class Meta:
        db_table = "works"
        verbose_name = "Произведения"
        verbose_name_plural = "Произведения"
        
        # это поле определяет сортировку работа в БД
        # порядок будет такой: Самые свежие будут сверху.
        ordering = ["-updated_at"]
    
    # название произведения на русском язке | обязательное поле
    title_ru = models.CharField(
        "Название на русском", 
        max_length=512,
        help_text="Например: Re:Zero. Жизнь с нуля в альтернативном мире"
    )

    # название произведения на языке оригинала Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu
    # необязательное поле
    title_orig = models.CharField(
        "Название на языке оригинала",
        max_length=512,
        blank=True,
        help_text="Например: Re:Zero kara Hajimeru Isekai Seikatsu"
    )
    
    # описание произведения | необязательное  поле
    description = models.TextField("Описание", blank=True) 
    
    # обложка произведения | обязательное поле
    cover_path = models.ImageField("Обложка", upload_to="works/covers/")

    # рейтинг произведения | Необязательное поле
    rating = models.DecimalField(
        "Рейтинг",
        max_digits=4,
        decimal_places=2,
        blank=True,
        default=0.00,
        help_text="Рейтинг произведения. Это значение лучше не трогать руками"
    )
    
    help_slug = \
    """
        Значения этого поля Django генерирует автоматически.
        Оно строится на основе поля: Название на русском.
        Оно нужно для красивого URL, а не абстрактного: wokr_id=322
        
        Например: 
            Из названия:  Re:Zero. Жизнь с нуля в альтернативном мир
            Получим slug: rezero-zhizn-s-nulya-v-alternativnom-mire
    """
    # слаг поле определяет название произведения URL ссылке
    # вычисляется автоматически Django
    slug = models.SlugField(
        "Слаг", 
        max_length=255, 
        unique=True,
        help_text=help_slug
    )
    
    # счетчик просмотров произведения
    views_count = models.PositiveBigIntegerField(
        "Просмотры", 
        default=0,
        help_text="Счетчик просмотров. Руками это лучше не трогать.",
        blank=True
    )
    
    # счетчик лайков
    likes_count = models.PositiveIntegerField(
        "Лайки", 
        default=0,
        help_text="Счетчик лайков. Руками это лучше не трогать.",
        blank=True
    )
    
    # счетчик фаворитов(сколько юзеров добавило произведение в фавориты)
    favorites_count = models.PositiveIntegerField(
        "В избранном", 
        default=0,
        help_text="Счетчик людей которые добавили данное произведение в избранное. Руками это лучше не трогать.",
        blank=True
    )

    # опубликовано ли произведение на сайте(видят ли его юзеры)
    is_published = models.BooleanField(
        "Опубликовать на сайте", 
        default=True,
        help_text="Данное поле определяет будет ли произведение показано на сайте."
    )
    
    # когда создал произведение админ на сайте
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    # когда админ в последний раз обновлял произведение
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    
    # дата и время публикации произведения на сайте
    published_at = models.DateTimeField("Опубликовано", blank=True, null=True)
    
    # ====================== СВЯЗИ ОДИН КО МНОГИМ ======================
    # id типа произведения(Ранобэ, фанфик и т. п.)
    # хочу заметить, что django под капотом
    # назовет это поле как work_type_id и просто
    # поля work_type существовать в БД не будет.
    # однако в коде, ты все равно будешь работать через
    # имя work_type. | Обязательное поле
    work_type = models.ForeignKey(
        WorkType,
        on_delete=models.PROTECT, # защищен от удаления, если есть ссылки
        verbose_name="Тип произведения",
        # немног потноватый параметр
        # он определяет имя через которое мы можем
        # получить ВСЕ произведения которые являются данным жанром
        related_name="works",
        help_text="Ранобэ, фанфик, и т. п."
    )

    # статус произведения(вышел, выходит, анонс и т. п.)
    # если попытаться удалить запись у которой есть связи - возникнет ошибка
    # Обазятельное поле
    status = models.ForeignKey(
        WorkStatuse,
        on_delete=models.PROTECT,
        verbose_name="Статус",
        related_name="works",
        help_text="Вышло, выходит, анонс, и т. п."
    )
    
    # возрастной рейтинг произведения | Необязательное поле
    # если попытаться удалить запись у которой есть связи - возникнет ошибка
    age_rating = models.ForeignKey(
        AgeRating,
        on_delete=models.PROTECT,
        verbose_name="Возрастной рейтинг",
        related_name="works",
        blank=True,
        help_text="R-17, G, PG, PG-13, R, NC-17, и т. п."
    )
    
    # язык оригинала | Необязательное поле.
    # если попытаться удалить запись у которой есть связи - возникнет ошибка
    orig_lang = models.ForeignKey(
        WorkOriginalLanguage,
        on_delete=models.PROTECT,
        verbose_name="Язык оригинала",
        related_name="works",
        null=True,
        help_text="Китайский, Японский, и т. п."
    )
    # ==================================================================
    
    # ===================== СВЯЗИ МНОГИЕ КО МНОГИМ =====================
    # автор или авторы произведения | Обязательное поле
    authors = models.ManyToManyField(
        Author,
        verbose_name="Авторы",
        related_name="works",
    )
    
    # фандом или фандомы произведения | Необязательное поле.
    fandoms = models.ManyToManyField(
        Fandom,
        verbose_name="Фандомы",
        related_name="works",
        blank=True,
        help_text="Наруто, Гарри Поттер, и т. п."
    )
    
    # жанры произведения | Обязательное поле 
    genres = models.ManyToManyField(
        Genre,
        verbose_name="Жанры",
        related_name="works",
        help_text="Фэнтези, Триллер, и т. п.",
    )
    
    # темы произведения | Необязательное поле
    themes = models.ManyToManyField(
        Theme,
        verbose_name="Темы",
        related_name="works",
        blank=True,
        help_text="Исэкай, Историческая, и т. п."
    )
    
    # автор или авторы перевода или команда перевода | Необязательное поле
    translators = models.ManyToManyField(
        Translator,
        verbose_name="Авторы перевода",
        related_name="works",
        blank=True,
        help_text="AI, RanobeList, и т. п."
    )
    # ==================================================================
    
    def __str__(self) -> str:
        return self.title_ru
    
    def save(self, *args, **kwargs) -> None:
        """
            Смысл данного метода детально описан у Chapter.
            
            Тут же, логика расширения заключается в установке
            времени публикации: published_at только тогда
            когда произведение действительно было опубликовано.
        """
        # self.pk - это id произведения
        # то есть, если проивездение уже существует
        if self.pk:
            old = Work.objects.get(pk=self.pk)
            
            # установить публикацию
            # если объект в БД еще не опубликован, но у того
            # который сейчас пушат is_published=True(то есть админ опубликовывает)
            # то меняем published_at
            if not old.is_published and self.is_published:
                self.published_at = timezone.now()
                
            # убрать публикацию
            elif old.is_published and not self.is_published:
                self.published_at = None
        
        # если произведение создается сразу опубликованным   
        else:
            if self.is_published and not self.published_at:
                self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def created_at_local(self):
        """Данный метод форматирует дату и время создания в привычный RU формат"""
        return localtime(self.created_at).strftime(r"%d.%m.%Y %H:%M")
    
    def updated_at_local(self, obj):
        """Данный метод форматирует дату и время изменения в привычный RU формат"""
        return localtime(obj.updated_at).strftime(r"%d.%m.%Y %H:%M")
    
    def published_at_local(self):
        """Данный метод форматирует дату и время публикации произведения в привычный RU формат"""
        if not self.published_at:
            return '-'
        return localtime(self.published_at).strftime(r"%d.%m.%Y %H:%M")
    
    def short_description(self) -> str:
        """
            Данный метод сокращает описание произведения в админке.
            Это нужно, чтобы само описание жестко не спамилось в админке,
            ибо оно может занимать довольно много места.
        """
        if not self.description:
            return '-'
        text = self.description.strip()
        return text[:10] + "..." if len(text) > 10 else text
    
    def cover_preview(self) -> str | SafeText:
        """
            Данный метод нужен для превью обложки 
            произведения в админке. Чтобы в поле картинки
            стояла картинка, а не просто путь.
        """
        if not self or not self.pk:
            return "Сначала сохраните произведение."
        if not self.cover_path:
            return "Обложка не загружена."
        return format_html(
            '<img src="{}" style="max-height: 300px; max-width: 220px; border: 1px solid #ccc;" />',
            self.cover_path.url
        )
    
    
class Chapter(models.Model):
    """
        В данной таблице хранятся все главы всех 
        произведений.

        Любая глава связана с таблицей Works к 
        какому-то произведению через связь:
        works_id -> Works.id
    """
    
    class Meta:
        db_table = "chapters"
        verbose_name = "Глава"
        verbose_name_plural = "Главы"
        ordering = ["work_id", "order_num"]

        # это ограничение на уникальность пары
        # (work_id, order_num) это нужно чтобы
        # не допускалось создание дублей, что у одного
        # произведения, есть 2 и более глав которые имеют
        # одинаковые order_num, это не допустимо.
        constraints = [
            models.UniqueConstraint(
                fields=["work", "order_num"],
                name="unique_chapter_order_per_work"
            )
        ]
        
    # произведение к которому принадлежит глава
    # при удалении произведения(Works), главы удалятся
    # автоматически.
    # история с именем тут та же, что и у других ForeignKey 
    # из таблицы Works, имя в БД будет work_id, а не work
    # Обязательное поле
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name="chapters",
        verbose_name="Произведение"
    )
    
    # название главы | Обязательное поле
    title =  models.CharField("Название главы", max_length=255)
    
    # порядковый номер который определяет порядок следования глав
    # в произведении. А потому, данное поле очень важно.
    # если оно будет заполняться не правильно, то порядок(структура)
    # произведения будет нарушена. | Необязательное поле
    order_num = models.PositiveIntegerField(
        "Порядковый номер главы",
        null=True,
        blank=True
    )
    
    # тут хранится сам текст(контент) главы произведения
    # обязательное поле
    content = models.TextField("Текст")
    
    # когда глава произведения была создана админом
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    
    # когда глава произведения была обновлена админом
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    
    # когда глава была опубликована
    published_at = models.DateTimeField("Опубликовано", auto_now_add=True)
      
    def save(self, *args, **kwargs):
        """
            Данные метод очень важен для удобного функционала модели.
            
            Стандартное поведение Django:
                work = Work(title="Test")
                work.save()
                
                Django под капотом делает это:
                    INSERT INTO works (title) VALUES ("Test")
                То есть генерирует такой SQL запрос на создание новой записи.
                
                А если сделать так:
                
                work.title = "New"
                work.save()
                
                То Django под капотом сделает это:
                    UPDATE works SET title="New" WHERE id=...
                
                Django умеет определять создали ли мы новый объект(в таком
                случае, нужно добавить совершенно новую запись в БД) или
                просто обновляем уже старый(существующий) объект. 
            
            Данный метод РАСШИРЯЕТ стандартное поведение, то есть Django,
            не лишился поведения которое описано выше, просто перед тем,
            как выполнить стандартное поведение он выполнит нечто, что
            уже написал я в этом методе.
            
            Теперь конкретно о том, что данный метод расширяет.
            
            Данный метод подсчитывает поле order_num автоматически.
            Например, админ создал карточку Re:Zero, и добавляет 1-ую главу.
            Штука в том, что админу необязательно вообще прописывать order_num
            вручную, данный метод считает order_num автоматически.
            Если order_num не указан в добавляемой главе то:
                1) Если глав у произведения нет вообще.
                    * Устанавливаем номер главы - 1.
                2) Если главы у произведения уже есть.
                    * Тогда берем номер максимальной главы и устанавливамем
                      новой главе: max_order_num + 1.
            
            А после подсчета order_num выполняется стандартное Django
            поведение(описано выше в примере) для этого метода.
        """
        
        # если админ не установил order_num у произведения
        if self.order_num is None:
            # тогда смотрим максимальный номер главы
            # у произведения(если они вообще есть)
            max_order = (
                Chapter.objects
                .filter(work=self.work)
                .aggregate(max_order=Max("order_num"))["max_order"]
            )
            # если нет номера, то 1, если есть то делаем +1
            self.order_num = 1 if max_order is None else max_order + 1

        # вызываем стандартное  Django поведение
        super().save(*args, **kwargs)
    
    
    