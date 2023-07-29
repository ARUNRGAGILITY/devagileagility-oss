from django.urls import path, include
#from . import views
from .views.todolist_views import *
from .views.typelist_views import *

urlpatterns = [
    path('big_picture',big_picture, name='big_picture'),
    path('toplevels_home',toplevels_home, name='toplevels_home'),
    path('add_mapping',add_mapping, name='add_mapping'),

    path('',todolist_home, name='todolist_home'),
    path('list',list_todolist, name='list_todolist'),
    path('topic_edit/<int:pk>',newtodolist_edit, name='edit_todolist'),
    path('topic_delete/<int:pk>',newtodolist_delete, name='delete_todolist'),
    path('sorted_todolist',newtodolist_sorted, name='sorted_todolist'),

    path('newtodolistitems/<int:pk>',list_newtodolistitems, name='list_newtodolistitems'),
    path('display_newtodolistitems/',main_display_tree, name='display_newtodolistitems'),
    path('display_todolist_as_table/',display_todolist_as_table, name='display_todolist_as_table'),
    path('display_todolist_as_table_id/<int:pk>',display_todolist_as_table_id, name='display_todolist_as_table_id'),
    path('newtodolist_update/',newtodolist_update, name='newtodolist_update'),

    path('clone_newtodolistitems/<int:pk>',clone_newtodolistitems, name='clone_newtodolistitems'),
    path('deepclone_newtodolistitems/<int:pk>',deepclone_newtodolistitems, name='deepclone_newtodolistitems'),

    ## typelist related
    path('typelist_home',typelist_home, name='typelist_home'),
    path('typelist_edit/<int:pk>',typelist_edit, name='typelist_edit'),
    path('typelist_delete/<int:pk>',typelist_delete, name='typelist_delete'),
    path('sorted_typelist',sorted_typelist, name='sorted_typelist'),

    path('list_childtypelist/<int:pk>',list_childtypelist, name='list_childtypelist'),
    path('display_childtypelist/',typelist_display_tree, name='display_childtypelist'),
    path('display_typelist_as_table/',display_typelist_as_table, name='display_typelist_as_table'),
    path('display_typelist_as_table_id/<int:pk>',display_typelist_as_table_id, name='display_typelist_as_table_id'),
    path('typelist_update/',typelist_update, name='typelist_update'),

    path('clone_typelist/<int:pk>',clone_typelist, name='clone_typelist'),
    path('deepclone_typelist/<int:pk>',deepclone_typelist, name='deepclone_typelist'),

]