from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import CommentForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, reverse
from .models import Campaign, Rating, ProjectComment, Picture, Tag, User_Donation,Category,User_Report_Project
from .forms import DonationForm, AddNewProduct, RatingForm,CategoryForm,TagForm,EditProduct
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg

#### all projects page and user is sent to show and hide update project button
def all_project(request):
    user=request.user
    projects = Campaign.objects.all()
    return render(request, 'campaignapp/allprojects.html', {'allpro': projects,'user':user})

#to prevent the user from entering add project from the url until he is logged in
@login_required(login_url='/accounts/login/')
def add_project(request):
    if request.method == "POST":
        newProject = AddNewProduct(request.POST, request.FILES)
        if newProject.is_valid():
            new_project = newProject.save(commit=False)
            tag_ids = request.POST.getlist('tags')

            new_project.creator_id = request.user.pk
            new_project.save()
            for picture_file in request.FILES.getlist('pictures'):
                if not picture_file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    newProject.add_error(None,'Only image files (JPEG, PNG, GIF) are allowed.')
                    
                else:
                    picture = Picture(image=picture_file)
                    picture.save()
                    new_project.pictures.add(picture)
            new_project.tags.set(tag_ids)

            return redirect('all_project')
    else:
        newProject = AddNewProduct()
    return render(request, 'campaignapp/addproject.html', {'form': newProject})


@login_required(login_url='/accounts/login/')
def DetailView(request, id):
    projectDetails = get_object_or_404(Campaign, pk=id)
    comments = ProjectComment.objects.filter(project=projectDetails)
    comment_form = CommentForm()
    donation_form = DonationForm()
    Total_Target = projectDetails.total_target
    project_donation = projectDetails.donation
    user = request.user
    rating_form = RatingForm()
    Related_Projects=[]
    Project_Reports=User_Report_Project.objects.filter(project=projectDetails,user=user)
    for Tag in projectDetails.tags.all():
        projects=Campaign.objects.filter(tags=Tag).exclude(title=projectDetails)
        for pro in projects:
            Related_Projects.append(pro)
    four_Projects=Related_Projects[:4]


    if project_donation < (Total_Target * 0.25):
        status = True
    else:
        status = False


    view_rate = Rating.objects.filter(user=user, project=projectDetails)
    if view_rate :
        rate_status = True
    else:
        rate_status = False
    
    if Project_Reports:
        reported_by_this_user=True
    else:
        reported_by_this_user=False

    return render(request, 'campaignapp/showDetails.html', {'rate_status': rate_status ,'RelatedProjects':four_Projects,'reported_by_this_user':reported_by_this_user,'rating_form': rating_form, 'comment_form': comment_form, 'user': user, 'donation_form': donation_form, 'projectdetails': projectDetails, 'comment': comments, 'status': status})


@ login_required(login_url='/accounts/login/')
def updateProduct(request, id):
    myproducts = get_object_or_404(Campaign, pk=id)
    if myproducts.creator != request.user:
        return render(request,'campaignapp/CantUpdate.html')
    else:
        if request.method == 'GET':
            form = EditProduct(instance=myproducts)
            return render(request, 'campaignapp/update.html', context={'form': form})
        if request.method == 'POST':
            Productform = EditProduct(
                request.POST, request.FILES, instance=myproducts)
            if Productform.is_valid():
                product = Productform.save(commit=False)
                tag_ids = request.POST.getlist('tags')
                for picture_file in request.FILES.getlist('pictures'):
                    picture = Picture.objects.create(image=picture_file)
                    product.pictures.add(picture)
                product.tags.set(tag_ids)
                product.save()
                return redirect('/projects')
            else:
                form=Productform
                return render(request, 'campaignapp/update.html', context={'form': form})


    return redirect('/projects')


@ login_required(login_url='/accounts/login/')
def deleteProduct(request, id):
    record = Campaign.objects.get(pk=id)
    if record.creator != request.user:
        return render(request, 'campaignapp/CantDelete.html')
    else:
        record.delete()
    return redirect('/projects')


@ login_required(login_url='/accounts/login/')
def add_rating(request, id):
    project = get_object_or_404(Campaign, pk=id)
    ratings = project.ratings.all()

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.cleaned_data['rating']
            if rating > 5:
                messages.error(request, 'Rating should not be more than 5.')
            else:
                Rating.objects.create(
                    user=request.user, project=project, rating=rating)
                avg_rating = ratings.aggregate(
                    avg_rating=Avg('rating'))['avg_rating']
                project.avg_rating = avg_rating
                project.save()
            return redirect('project_detail', id=project.pk)

    else:
        rating_form = RatingForm()

    avg_rating = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
    context = {
        'rating_form': rating_form,
        'project': project,
        'avg_rating': avg_rating,
    }
    return render(request, 'campaignapp/showDetails.html', context)


@ login_required(login_url='/accounts/login/')
def addComment(request, id):
    project = get_object_or_404(Campaign, pk=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment_text = request.POST['comment_text']
            comment = ProjectComment.objects.create(user=request.user, project=project, comment_text=comment_text)
            comment.save()
            return redirect('project_detail', id=project.pk)
    return render(request, 'campaignapp/showDetails.html', {'projectdetails': project, 'comment_form': comment_form})


@ login_required(login_url='/accounts/login/')
def report_comment(request, id):
    if request.method == 'POST':
        comment = get_object_or_404(ProjectComment, pk=id)
        comment.is_reported = True
        comment.save()
    return redirect('project_detail', id=comment.project.pk)


@ login_required(login_url='/accounts/login/')
def addDonation(request, id):
    project = get_object_or_404(Campaign, pk=id)
    Total_Target = project.total_target
    project_donation = project.donation
    if request.method == 'POST':
        donation_form = DonationForm(request.POST)
        if donation_form.is_valid():
            donation_amount = float(request.POST.get('donate'))
            project_donation += donation_amount
            project.donation = project_donation
            project.save()
            user_donation = User_Donation(user=request.user,project=project,donate=donation_amount,)
            user_donation.save()
            return redirect('project_detail', id=project.pk)

    return render(request, 'campaignapp/showDetails.html', {'projectdetails': project,  'donation_form': donation_form, 'total_target': Total_Target})


@ login_required(login_url='/accounts/login/')
def reportProject(request, id):
    if request.method == 'POST':
        project_to_be_Reported = get_object_or_404(Campaign, id=id)
        User_Report_Project.objects.create(user=request.user, project=project_to_be_Reported)
        project_to_be_Reported.save()
    return redirect('project_detail', id=project_to_be_Reported.pk)


@ login_required(login_url='/accounts/login/')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/projects')
    else:
        form = CategoryForm()
    return render(request, 'campaignapp/addcategory.html', {'form': form})


@ login_required(login_url='/accounts/login/')
def add_tag(request):
    if request.method == 'POST':
        form=TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/projects')
    else:
        form=TagForm()
    return render(request, 'campaignapp/addtag.html', {'form': form})