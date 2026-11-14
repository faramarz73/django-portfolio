from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """اطلاعات اصلی سایت (فقط یک رکورد بسازید)."""
    name = models.CharField("نام", max_length=100)
    headline = models.CharField("عنوان اصلی صفحه", max_length=200,
                                default="ربات تلگرام، وب‌سایت و اپلیکیشن؛ از ایده تا اجرا")
    bio = models.TextField("معرفی کوتاه", blank=True)
    contact_url = models.URLField("لینک سفارش/ارتباط (مثلاً آیدی تلگرام)", blank=True)

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("نام دسته", max_length=60)
    slug = models.SlugField("اسلاگ (انگلیسی)", unique=True, allow_unicode=False)
    order = models.PositiveIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField("عنوان", max_length=120)
    slug = models.SlugField("اسلاگ (انگلیسی)", unique=True)
    category = models.ForeignKey(Category, verbose_name="دسته", on_delete=models.PROTECT,
                                 related_name="projects")
    summary = models.CharField("خلاصه", max_length=220)
    description = models.TextField("توضیحات کامل", blank=True)
    image = models.ImageField("تصویر", upload_to="projects/", blank=True)
    link = models.URLField("لینک پروژه (ربات، سایت یا اپ)", blank=True)
    tags = models.CharField("تکنولوژی‌ها (با کاما جدا کنید)", max_length=200, blank=True,
                            help_text="مثال: Python, aiogram, Django")
    featured = models.BooleanField("ویژه", default=False)
    order = models.PositiveIntegerField("ترتیب", default=0)
    created = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created"]
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("works:detail", args=[self.slug])

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class SocialLink(models.Model):
    name = models.CharField("نام شبکه", max_length=40)
    url = models.URLField("لینک")
    order = models.PositiveIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه‌های اجتماعی"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField("عنوان", max_length=160)
    slug = models.SlugField("اسلاگ (انگلیسی)", unique=True)
    summary = models.CharField("خلاصه", max_length=240)
    body = models.TextField("متن مقاله")
    cover = models.ImageField("تصویر شاخص", upload_to="posts/", blank=True)
    published = models.BooleanField("منتشر شود", default=True)
    created = models.DateTimeField("تاریخ انتشار", auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "مقاله"
        verbose_name_plural = "وبلاگ"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("works:post", args=[self.slug])


class Order(models.Model):
    TYPES = [("bot", "ربات تلگرام"), ("web", "وب‌سایت"), ("app", "اپلیکیشن"), ("other", "سایر")]
    name = models.CharField("نام", max_length=100)
    contact = models.CharField("راه تماس (آیدی تلگرام / ایمیل / شماره)", max_length=120)
    kind = models.CharField("نوع پروژه", max_length=10, choices=TYPES, default="bot")
    budget = models.CharField("بودجهٔ تقریبی", max_length=60, blank=True)
    message = models.TextField("توضیح پروژه")
    handled = models.BooleanField("بررسی شد", default=False)
    created = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"

    def __str__(self):
        return f"{self.name} - {self.get_kind_display()}"
