from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout, login as auth_login
from django.contrib import messages
from .models import Checker,Maker,CustomerProfile,cutomerUser
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


# Create your views here.
def checkeregister(request):
    return render(request,'checker_register.html')

    
def loginpage(request):
    return render(request,'login.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Received username: {username}, password: {password}")  # Debug print

        user = authenticate(request, username=username, password=password)
        
        print(user)  # Debug print to check the user object

        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('/')
            elif user.is_checker:
                return redirect('checkerpage')
            elif user.is_maker:
                return redirect('makerpage')
            else:
                messages.error(request, 'Invalid user role')
        else:
            print("Authentication failed!")  # Debug print
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


from django.contrib.auth import get_user_model

def add_checker(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        address = request.POST['address']
        gender = request.POST['radio']
        joined_date = request.POST['joined_date']
        emailid = request.POST['emailid']

        User = get_user_model()


        if User.objects.filter(username=username).exists():
            return render(request, 'checker_register.html', {'error_message': 'Username already exists'})

        user =User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            password=password,
            email=emailid,
        )
        user.is_checker = True
        user.save()

        checker = Checker(
            user=user,
            firstname=firstname,
            lastname=lastname,
            address=address,
            gender=gender,
            emailid=emailid,
            joined_date=joined_date
        )
        checker.save()

        return redirect('loginpage')
    return render(request, 'checker_register.html')
# def adminpage(request):
#     pending_checkers = Checker.objects.filter(approved=False)
#     return render(request, 'admin.html', {'pending_checkers': pending_checkers})

# @require_POST
# def approve_checker(request, checker_id):
#     checker = get_object_or_404(Checker, id=checker_id)
#     checker.approved = True
#     checker.save()
#     # return redirect('adminpage')
#     return render(request, 'admin.html')

# @require_POST
# def reject_checker(request, checker_id):
#     checker = get_object_or_404(Checker, id=checker_id)
#     checker.delete()
#     return render(request, 'admin.html')


    
def maker_register(request):
    checkers = Checker.objects.all()
    return render(request,'makerregister.html' ,{'checkers' : checkers})

def add_maker_register(request):
    if request.method == 'POST':
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        username = request.POST['username']
        password = request.POST['password']
        gender = request.POST['inlineRadioOptions']
        joined_date = request.POST['date']
        emailid = request.POST['email']
        checker_id = request.POST['checker_select']
        checker = get_object_or_404(Checker, id=checker_id)

        User = get_user_model()

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'makerregister.html', {'error_message': 'Username already exists'})

        # Create the new user
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            password=password,
            email=emailid,
        )
        user.is_maker = True
        user.save()

        # Create the Maker entry and associate it with the user
        maker = Maker(
            user=user,  # Associate the maker with the created user
            fname=firstname,
            lname=lastname,
            gender=gender,
            email_id=emailid,
            joined_date=joined_date,
            checker=checker
        )
        maker.save()

        return redirect('loginpage')
    return render(request, 'makerregister.html')

def checkerpage(request):
    try:
        checker = Checker.objects.get(user=request.user)
    
    except Checker.DoesNotExist:
        # Handle the case where the associated checker does not exist
        checker = None
    
   

    return render(request, 'userlogin.html', {'checker': checker})

def makerpage(request):
    try:
        maker = Maker.objects.get(user=request.user)
        checker = maker.checker  # Access the associated checker directly from the maker object
    except Maker.DoesNotExist:
        # Handle the case where the maker does not exist
        checker = None
    except Checker.DoesNotExist:
        # Handle the case where the associated checker does not exist
        checker = None
    
  
    return render(request, 'makerpage.html',{'checker':checker})


def createcustomer(request):
    try:
        maker = Maker.objects.get(user=request.user)
        checker = maker.checker  # Access the associated checker directly from the maker object
    except Maker.DoesNotExist:
        # Handle the case where the maker does not exist
        checker = None
    except Checker.DoesNotExist:
        # Handle the case where the associated checker does not exist
        checker = None
    
    return render(request, 'custmercreate.html', {'checker': checker})


from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.urls import reverse


@login_required
def create_profile(request):
    if request.method == 'POST':
        try:
            maker = Maker.objects.get(user=request.user)
            checker = maker.checker  # Access the checker directly from the maker object
        except ObjectDoesNotExist:
            return HttpResponse("Maker or Checker object does not exist. Please contact support.")
        except Exception as e:
            return HttpResponse(f"An unexpected error occurred: {str(e)}")

        form_data = {
            'username': request.POST.get('user', ''),
            'email': request.POST.get('mail', ''),
            'qualification': request.POST.get('qualification', ''),
            'gender': request.POST.get('gender', ''),
            'age': request.POST.get('age', '')
        }
        
        resume = request.FILES.get('resume')
        image = request.FILES.get('image')

        try:
            resume_name = None
            if resume:
                fs = FileSystemStorage()
                resume_name = fs.save(resume.name, resume)

            image_name = None
            if image:
                fs = FileSystemStorage()
                image_name = fs.save(image.name, image)

            customer_profile = CustomerProfile(
                username=form_data['username'],
                email=form_data['email'],
                qualification=form_data['qualification'],
                gender=form_data['gender'],
                age=form_data['age'],
                resume=resume_name,
                image=image_name,
                checker=checker,
                maker=maker,
                status='pending'  # Default status
            )
            customer_profile.save()
            
            return redirect(reverse('customerdetails', args=[customer_profile.id]))  # Redirect to a success page
        except Exception as e:
            return HttpResponse(f"An unexpected error occurred while saving the profile: {str(e)}")

    return render(request, 'customercreate.html')


def customerdetails(request, id):
    checker = get_object_or_404(Checker, pk=id)  # Get the specific checker by ID
    maker=Maker.objects.get(user=request.user)
    customers = CustomerProfile.objects.filter(checker=checker, maker=maker)
    print('customer',customers)
    return render(request, 'custdetailsstatus.html', {'customers': customers, 'checker': checker})


def genicpage(request):
    return render(request,'genicpage.html')


def showcustdetails(request, id):
    checker = get_object_or_404(Checker, pk=id)  # Get the specific checker by ID
    # maker = Maker.objects.get(user=request.user)
    customers = CustomerProfile.objects.filter(checker=checker)
    return render(request, 'customerdetailschkr.html', {'customers': customers, 'checker': checker})


def approve_customer(request, id):
    customer = get_object_or_404(CustomerProfile, id=id)
    customer.status = 'approved'
    customer.save()
    return redirect('showcustdetails', id=customer.checker.id) 



def reject_customer(request, id):
    customer = get_object_or_404(CustomerProfile, id=id)
    customer.status = 'declined'
    customer.save()
    return redirect('showcustdetails', id=customer.checker.id)










    



