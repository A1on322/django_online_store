from django.contrib import admin
from django.utils.safestring import mark_safe

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_image')
    search_fields = ('email',)

    @admin.display(description='Image')
    def user_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")
        return 'No image'