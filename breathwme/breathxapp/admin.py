from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import SilentExercise
import json

class SilentExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_time', 'breaths', 'skill_level', 'shape')

    class Media:
        js = ('admin/vibration_editor.js',)  # Custom JavaScript for visual editor
        css = {'all': ('admin/vibration_editor.css',)}  # Custom CSS for visual editor

    def vibration_editor(self, obj):
        return mark_safe("""
        <div style="margin-bottom: 10px;">
            <strong>Vibration Timeline (Click to Add Vibration Cues)</strong>
        </div>
        <div id="vibration-editor" style="width:100%;height:50px;background:#ddd;border:1px solid #ccc;position:relative;">
        </div>
        <input type="hidden" id="vibration-cues" name="vibration_cues">
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            let editor = document.getElementById('vibration-editor');
            let input = document.getElementById('vibration-cues');
            let cues = JSON.parse(input.value || '[]');

            function renderCues() {
                editor.innerHTML = '';
                cues.forEach((cue, index) => {
                    let el = document.createElement('div');
                    el.style.position = 'absolute';
                    el.style.left = (cue / obj.total_time) * editor.clientWidth + 'px';
                    el.style.width = '10px';
                    el.style.height = '100%';
                    el.style.background = 'red';
                    el.style.cursor = 'pointer';
                    el.dataset.index = index;
                    el.onclick = () => {
                        cues.splice(index, 1);
                        renderCues();
                    };
                    editor.appendChild(el);
                });
                input.value = JSON.stringify(cues);
            }

            editor.onclick = function(e) {
                let rect = editor.getBoundingClientRect();
                let time = ((e.clientX - rect.left) / editor.clientWidth) * obj.total_time;
                cues.push(time);
                renderCues();
            };

            renderCues();
        });
        </script>
        """)

    def save_model(self, request, obj, form, change):
        obj.vibration_cues = json.dumps(obj.vibration_cues)  # Ensure it's saved as a JSON field
        super().save_model(request, obj, form, change)

admin.site.register(SilentExercise, SilentExerciseAdmin)


from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "date", "time", "is_approved")
    list_filter = ("is_approved",)
    search_fields = ("name", "email")
    readonly_fields = ("name", "email", "message", "date", "time")  # Prevent modification

    def save_model(self, request, obj, form, change):
        if obj.is_approved and obj.zoom_link:  # Ensure Zoom link is added when approving
            obj.save()
        else:
            obj.is_approved = False  # Prevent approval without a Zoom link
            obj.save()

admin.site.register(Booking, BookingAdmin)
