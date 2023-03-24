
# Create your views here.
from django import forms

from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Users
from accounts.Forms import Register, OptionalInfoForm, UserUpdatedOptionalForm
from campaignapp.models import Campaign, User_Donation
from homepage.views import slide_project


@login_required(login_url='/accounts/Login.html')
def userprofile(request, id):
    user = Users.objects.get(id=id)
    # 1 projects
    project = Campaign.objects.filter(
        creator=user)
    # 2 donations
    donation = User_Donation.objects.filter(
        user=user)

    return render(request, "users/show.html", context={'user': user, 'projects': project, 'donations': donation})


# edit user data execpt email

class edit(UpdateView):
    model = Users
    template_name = 'users/edit.html'
    form_class = UserUpdatedOptionalForm
    success_url = 'show'

    def form_valid(self, form):
        password1 = form.cleaned_data.get('Password')
        password2 = form.cleaned_data.get('RepeatPassword')
        image = form.cleaned_data.get('image')
        mobile_phone = form.cleaned_data.get('mobile_phone')
        firstname = form.cleaned_data.get('firstname')
        lastname = form.cleaned_data.get('lastname')

        #  to check that the image field is not empty
        if not image:
            form.add_error('image', 'Please upload an image')
            return self.form_invalid(form)
        if not firstname:
            form.add_error('firstname', 'Please enter first name')
            return self.form_invalid(form)

        if not lastname:
            form.add_error('lastname', 'Please enter last name')
            return self.form_invalid(form)

        if not mobile_phone:
            form.add_error('mobile_phone', 'Please enter mobile phone number')
            return self.form_invalid(form)

        # to make sure that the file enterd is only image

        if password1 != password2:
            form.add_error('RepeatPassword', "Passwords don't match")
            return self.form_invalid(form)
        mobile_phone = form.cleaned_data.get('mobile_phone')
        if Users.objects.exclude(pk=self.object.pk).filter(mobile_phone=mobile_phone).exists():
            form.add_error(
                'MobilePhone', 'This mobile phone number is already taken')
            return self.form_invalid(form)

        return super().form_valid(form)


class More(UpdateView):
    model = Users
    template_name = 'users/moreInfo.html'
    form_class = OptionalInfoForm
    success_url = 'show'


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_account(request, id):
    u = Users.get_specific_info(id)
    delete_form1 = u.Password
    if request.method == "POST":
        delete_form = Users.get_specific_info(id)
        delete_form1 = delete_form.Password

        if delete_form1:
            entered_password = request.POST['password']
            try:
                user = Users.objects.get(id=u.id)
            except ObjectDoesNotExist:
                return render(request, 'users/delete_account.html', {
                    'form': delete_form,
                    'message': 'account does not exist'
                })

            if delete_form1 == entered_password:
                user.delete()
                return redirect('home')
            else:
                return render(request, 'users/delete_account.html', {
                    'form': delete_form,
                    'message': 'Invalid password'
                })

    else:
        pass
    return render(request, "users/delete_account.html")
