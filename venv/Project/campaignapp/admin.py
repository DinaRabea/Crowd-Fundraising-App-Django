from django.contrib import admin
from .models import Category, Tag, Picture, Campaign, ProjectComment, Rating, User_Donation,User_Report_Project


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Picture)
admin.site.register(Campaign)
admin.site.register(ProjectComment)
admin.site.register(Rating)
admin.site.register(User_Donation)
admin.site.register(User_Report_Project)
