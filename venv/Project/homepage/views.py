from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from campaignapp.models import Category, Tag, Picture, Campaign, ProjectComment, Rating


def slide_project(request):
    dataorder = Campaign.objects.order_by('-avg_rating')[:5]
    lastprojects = Campaign.objects.all().order_by('-id')[:5]
    activeByadmin = Campaign.objects.all().filter(
        is_Featured=True).order_by('-id')[:5]
    allcategory = Category.objects.all()

    return render(request, 'homepage/home.html', {'projectAll': lastprojects,  'activeByadmin': activeByadmin, 'ordering': dataorder, 'allcategory': allcategory})


def list_category(request, id):
    category=Category.objects.get(pk=id)
    projects_Cat = Campaign.objects.filter(category=id)
    return render(request, 'homepage/categoryprojects.html', {'projectAll': projects_Cat,'category':category})


def search_results(request):
    search_type = request.GET.get('search_type')
    query = request.GET.get('query', '')

    if search_type == 'tags':
        
        Tags = Tag.objects.filter(name__icontains=query)        
        projects = Campaign.objects.filter(tags__in=Tags)
        projects=set(projects)
    elif search_type == 'titles':
        projects = Campaign.objects.filter(title__icontains=query)

    context = {'projects': projects,
               'query': query, 'search_type': search_type}
    return render(request, 'homepage/search_results.html', context)

