from django.urls import path
from .views import editor, save_chapter


urlpatterns = [
    path("editor/<slug:slug>/<int:chapter_id>/", editor, name="editor"),
    path("editor/<slug:slug>/new/", editor, name="editor"),
    path("save_chapter/<slug:slug>/<int:chapter_id>/", save_chapter, name="save_chapter"),
    path("save_chapter/<slug:slug>/new/", save_chapter, name="save_chapter")
    
]