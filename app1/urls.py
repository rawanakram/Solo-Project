from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('filtercontractors',views.filter_contractors),
    path('loginreg',views.loginreg),
    path('register',views.register),
    path('login',views.login),
    path('contractors',views.contractors),
    path('filter',views.filter),
    path('contractordetails/<int:contractor_id>',views.contractordetails),
    path('updateinfo/<int:contractor_id>',views.update_info),
    path('materialdetails/<int:material_id>/<int:contractor_id>',views.materialdetails),
    path('add',views.add),
    path('addmaterial',views.addmaterial),
    path('edit/<int:material_id>',views.edit),
    path('updatematerial/<int:material_id>',views.update_material),
    path('delete/<int:material_id>',views.delete),
    path('logout', views.logout)
]