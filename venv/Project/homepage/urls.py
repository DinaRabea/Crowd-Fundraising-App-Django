from django.urls import path
from homepage.views import slide_project, list_category, search_results
# from django.urls import url


urlpatterns = [

    path('', slide_project, name='home'),
    path('category/<int:id>', list_category, name='category'),

    path('search', search_results, name='search_results'),

]
