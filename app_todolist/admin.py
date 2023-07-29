from django.contrib import admin
from .models import *


class NewTodoListAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'title',  'author','active', 'done')
class TypeListAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'title', 'description',  'author','active')
admin.site.register(NewTodoList, NewTodoListAdmin)
admin.site.register(TypeList, TypeListAdmin)
admin.site.register(MappingTable)
