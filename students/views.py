from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Student, Register, Staff, Department
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request, 'students/main.html')


def application(request):
    return render(request, 'students/application.html')


def save(request):
    Student.objects.create(student_name=request.POST['name'], student_email=request.POST['email'],
                           student_phone=request.POST['phone'], ssc_marks=request.POST['ssc_marks'],
                           inter_marks=request.POST['inter_marks'])
    return HttpResponseRedirect('/students/')


def registration(request):
    deps = Department.objects.all()
    return render(request, 'students/register.html', {"deps": deps})


def save_details(request):
    if Student.objects.filter(student_email=request.POST['email'], is_verified=True).exists():
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        student = Student.objects.get(student_email=request.POST["email"])
        dep = Department.objects.get(code=request.POST['code'])
        Register.objects.create(image=request.FILES['image'], department=dep, user=user, Student=student)
        return HttpResponseRedirect('/students/')
    else:
        return render(request, 'students/application.html', {'error': 'you are not a valid user'})


def login_info(request):
    return render(request, 'students/login.html')


def validate(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/students/details/')
    else:
        return render(request, 'students/login.html', {'error': 'Invalid username or password'})


@login_required(login_url="/students/login/")
def details(request):
    user = request.user
    return render(request, 'students/details.html', {'user': user})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/students/login/')


def staff_registration(request):
    return render(request, 'students/staff.html')


def save_staffdetails(request):
    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
    # dep = Department.objects.get(code=request.POST['code'])
    Staff.objects.create(staff_name=request.POST['name'], staff_email=request.POST['email'],
                         staff_phone=request.POST['phone'], qualification=request.POST['qualification'],
                         staff_department=request.POST['department'],
                         experience=request.POST['experience'], photo=request.FILES['photo'], user=user)

    return HttpResponseRedirect('/students/')


def staff_validate(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        if Staff.objects.filter(user=user).exists():
            return HttpResponseRedirect('/students/staff_details/')
    else:
        return render(request, 'students/staff.html', {'error': 'you are not a valid user'})


def staff_login(request):
    return render(request, 'students/staff_login.html')


@login_required(login_url="/students/staff_login/")
def staff_detail(request):
    user = request.user
    return render(request, 'students/staff_details.html', {'user': user})


def staff_logout(request):
    logout(request)
    return HttpResponseRedirect('/students/staff_login/')


@login_required(login_url="/students/staff_login/")
def total_staff(request):
    staff = Staff.objects.all()
    return render(request, 'students/totalstaff.html', {'staff': staff})


@login_required(login_url="/students/login/")
def total_students(request):
    deps = Department.objects.all()
    return render(request, 'students/total_students.html', {"deps": deps})


def std_details(request, dep_code):
    student = Register.objects.filter(department__code=dep_code)
    return render(request, 'students/mechstudents.html', {'student': student})
