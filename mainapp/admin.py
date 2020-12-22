from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from PIL import Image

from .models import *


class NotebookAdminForm(ModelForm):

    MIN_RESOLUTION = (400, 400)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].help_text = "Загружайте изображения с минимальным разрешением {}x{}".format(*self.MIN_RESOLUTION)

    def clean_image(self):
        image = self.cleaned_data["image"]
        img = Image.open(image)
        min_width, min_height = self.MIN_RESOLUTION
        if img.width < min_width or img.height < min_height:
            raise ValidationError("Разрешение загруженного изображения меньше {}x{}".format(*self.MIN_RESOLUTION))
        return image

class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="notebooks"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="smartphones"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)