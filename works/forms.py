from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    # فیلد مخفی ضد اسپم: ربات‌ها پرش می‌کنند، انسان‌ها نه
    website = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"tabindex": "-1", "autocomplete": "off"}))

    class Meta:
        model = Order
        fields = ["name", "contact", "kind", "budget", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("spam")
        return ""
