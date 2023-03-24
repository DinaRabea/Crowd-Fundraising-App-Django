
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Users, Activation
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .Forms import Register, LoginForm
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UsersSerializer
from rest_framework import status


def AddUser(request):
    if request.method == 'POST':
        form = Register(request.POST, request.FILES)
        if form.is_valid():
            my_user = form.save(commit=False)
            my_user.image = request.FILES['image']
            form.save()
            activation = Activation.objects.create(
                user=my_user, expires_at=timezone.now() + timedelta(hours=24))
            activation_url = request.build_absolute_uri(
                reverse('activate', args=[str(activation.token)]))
            send_mail(
                'Activate your account',
                f'Please click the link below to activate your account:\n{activation_url}',
                'noreply@example.com',
                [my_user.Email],
                fail_silently=False,
            )
            return render(request, 'accounts/Registeration_done.html', {'user': my_user.Firstname, 'email': my_user.Email})
    else:
        form = Register()
    return render(request, "accounts/Signup.html", {'form': form})


def activate(request, token):
    activation = get_object_or_404(Activation, token=token)

    if activation.is_expired():
        activation.delete()
        return HttpResponse("Activation link has expired")

    user = activation.user
    user.is_active = True
    user.is_authenticated = True
    user.save()
    activation.delete()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    return render(request, 'accounts/Activated.html', {'user': user.Firstname, 'email': user.Email})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:

                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'accounts/Login.html', {'form': form})


@api_view(['GET', 'POST'])
def all_users(request):
    if request.method == 'GET':
        all_users = Users.objects.all()
        users_serializer = UsersSerializer(all_users, many=True)
        return Response(users_serializer.data)
    elif request.method == 'POST':
        user_serializer = UsersSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            user = Users.objects.get(pk=id)
            user.save()
            response_data = user_serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def one_user(request, id):
    one_user = Users.objects.all().get(id=id)
    if request.method == 'GET':
        ONe_User_Ser = UsersSerializer(one_user, many=False)
        return Response(ONe_User_Ser.data)
    elif request.method == 'PUT':
        one_ser = UsersSerializer(
            data=request.data, instance=one_user)
        if one_ser.is_valid():
            one_ser.save()
            return Response(one_ser.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        one_user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
