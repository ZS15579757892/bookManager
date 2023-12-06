from django.contrib import admin
from .models import Books, Record


# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'name', 's_time', 'e_time', 'state']


admin.site.register(Books, BooksAdmin)
admin.site.register(Record, RecordAdmin)
