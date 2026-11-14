import json
import os
import urllib.request

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Category, Post, Project


def home(request):
    categories = Category.objects.all()
    active = request.GET.get("cat", "")
    projects = Project.objects.select_related("category")
    if active:
        projects = projects.filter(category__slug=active)
    return render(request, "works/home.html",
                  {"projects": projects, "categories": categories, "active": active})


def detail(request, slug):
    project = get_object_or_404(Project.objects.select_related("category"), slug=slug)
    return render(request, "works/detail.html", {"project": project})


def blog(request):
    return render(request, "works/blog.html", {"posts": Post.objects.filter(published=True)})


def post(request, slug):
    p = get_object_or_404(Post, slug=slug, published=True)
    return render(request, "works/post.html", {"post": p})


def _notify_telegram(order):
    """اگر توکن و چت‌آیدی تنظیم شده باشد، سفارش جدید را به تلگرام خودتان می‌فرستد."""
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        return
    text = (f"سفارش جدید\nنام: {order.name}\nتماس: {order.contact}\n"
            f"نوع: {order.get_kind_display()}\nبودجه: {order.budget or '-'}\n\n{order.message}")
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=json.dumps({"chat_id": chat, "text": text}).encode(),
            headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # خطای اعلان نباید ثبت سفارش را خراب کند


def order(request):
    form = OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        _notify_telegram(obj)
        messages.success(request, "سفارش شما ثبت شد. به‌زودی با شما تماس می‌گیرم.")
        return redirect("works:order")
    return render(request, "works/order.html", {"form": form})
