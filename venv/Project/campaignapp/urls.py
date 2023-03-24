from django.urls import path
from . import views
urlpatterns = [
    path('', views.all_project, name="all_project"),
    path('add/', views.add_project, name="add_project"),
    path('show/<int:id>/', views.DetailView, name='project_detail'),
    path('edit/<int:id>/', views.updateProduct, name='project_update'),
    path('delete/<int:id>', views.deleteProduct, name='deleteproduct'),
    path('comment/<int:id>', views.addComment, name='add_comment'),
    path('report_comment/<int:id>', views.report_comment, name='report_comment'),
    path('donate/<int:id>', views.addDonation, name='add_donation'),
    path('add_rating/<int:id>', views.add_rating, name='add_rating'),
    path('reportProject/<int:id>', views.reportProject, name='report_project'),
    path('add_category',views.add_category,name='add_category'),
    path('add_tag',views.add_tag,name='add_tag'),

]
