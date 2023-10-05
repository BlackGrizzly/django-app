from django import forms
from django.core import validators
from .models import Product, Order

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "active", "preview"

    images = MultipleFileField()
    #name = forms.CharField(label="Наименование", max_length=100)
    #description = forms.CharField(
    #    label="Описание", 
    #    widget=forms.Textarea(attrs={"rows":5, "cols": 30}), 
    #    validators=[validators.RegexValidator(regex=r"great", message="Поле должно содержать слово 'great'")],
    #)
    #price = forms.DecimalField(label="Цена", min_value=0)
    #active = forms.BooleanField(default=False)
    #weight = forms.PositiveSmallIntegerField(default=0)
    #last_change_date = forms.DateTimeField(auto_now=True)
    #add_date = forms.DateTimeField(auto_now_add=True)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "user", "products", "delivery_address", "comment"

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
