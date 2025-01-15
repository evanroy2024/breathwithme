from django.contrib import admin
from .models import Course, Material , Item

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1  # Shows one empty form by default


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material_type', 'course', 'content_url', 'pdf_file', 'order')

admin.site.register(Course)
admin.site.register(Material, MaterialAdmin)

# admin.site.register(Item)
