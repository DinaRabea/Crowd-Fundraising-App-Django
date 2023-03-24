from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import Users


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Picture(models.Model):
    image = models.ImageField(upload_to='images/%y/%m/%d')


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pictures = models.ManyToManyField(Picture)
    total_target = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    donation = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    is_Featured = models.BooleanField(default=False)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.title


class Rating(models.Model):
    project = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class ProjectComment(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_reported = models.BooleanField(default=False)

    def __str__(self):
        return self.comment_text


class User_Donation(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    donate = models.PositiveIntegerField()


class User_Report_Project(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Campaign, on_delete=models.CASCADE)
