from django.urls import path, include
from . import views

urlpatterns = [

    ## this is the levels that can help to configure different levels for different work item types 
    # or source items

    path('', views.toplevel_home, name='toplevel_home'),
    path('levels', views.list_levels, name='list_levels'),
    path('levels_edit/<int:pk>', views.edit_levels, name='edit_levels'),
    path('levels_delete/<int:pk>', views.delete_levels, name='delete_levels'),
    path('sorted_levels', views.sorted_levels, name='sorted_levels'),

    path('newlevels/<int:pk>', views.list_newlevels, name='list_newlevels'),
    path('display_newlevels/', views.display_levelstree, name='display_newlevels'),
    path('display_levels_as_table/', views.display_levels_as_table, name='display_levels_as_table'),
    path('display_levels_as_table_id/<int:pk>', views.display_levels_as_table_id, name='display_levels_as_table_id'),
    path('newlevels_update/', views.newlevels_update, name='newlevels_update'),

    path('clone_newlevels/<int:pk>', views.clone_newlevels, name='clone_newlevels'),
    path('deepclone_newlevels/<int:pk>', views.deepclone_newlevels, name='deepclone_newlevels'),
]