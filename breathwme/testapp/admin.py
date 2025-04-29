# anotherapp/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from testapp.models import TestExercise, Category , Breathnameset # Import TestExercise from testapp

admin.site.register(Breathnameset)

@admin.register(TestExercise)
class TestExerciseAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        add_pattern_url = reverse('testapp:marking_beats', args=[object_id])
        extra_context = extra_context or {}

        # Pass the button HTML to the context
        extra_context['add_pattern_button'] = format_html(
            '''
            <div style="text-align: center; margin-top: 20px;">
                <a class="button" href="{}" style="
                    background-color: #1d68a7;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 4px;
                    text-decoration: none;
                    font-weight: bold;
                    display: inline-block;
                    width: auto;
                ">➕ Add Pattern</a>
            </div>
            ''',
            add_pattern_url
        )
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
