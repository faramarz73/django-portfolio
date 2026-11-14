from django.urls import path
from . import views

app_name = "works"
urlpatterns = [
    path("", views.home, name="home"),
    path("project/<slug:slug>/", views.detail, name="detail"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.post, name="post"),
    path("order/", views.order, name="order"),
]
