from django import template
from django.utils import timezone

register = template.Library()
MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
          "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    gy2 = gy + 1 if gm > 2 else gy
    days = (355666 + 365 * gy + (gy2 + 3) // 4 - (gy2 + 99) // 100
            + (gy2 + 399) // 400 + gd + g_d_m[gm - 1])
    jy = -1595 + 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm, jd = 1 + days // 31, 1 + days % 31
    else:
        jm, jd = 7 + (days - 186) // 30, 1 + (days - 186) % 30
    return jy, jm, jd


@register.filter
def jdate(value):
    """نمایش تاریخ شمسی، مثل: ۲۳ آبان ۱۴۰۵"""
    if not value:
        return ""
    if hasattr(value, "hour") and timezone.is_aware(value):
        value = timezone.localtime(value)
    jy, jm, jd = to_jalali(value.year, value.month, value.day)
    return f"{jd} {MONTHS[jm - 1]} {jy}".translate(DIGITS)
