from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse  ##
from django.contrib.auth import login, authenticate, logout
from .forms import UserSignUpForm, UserSignInForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Price
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'mysite/index.html')

def register(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('mysite/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
        else:
            return render(request, 'mysite/signup.html', {'form': form})
    else:
        form = UserSignUpForm()
    return render(request, 'mysite/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form = UserSignInForm(request.POST)
            return render(request, 'mysite/signin.html', {'form': form})
    else:
        form = UserSignInForm()
        return render(request, 'mysite/signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')

def plan_pricing(request):
    data = Price.objects.all()
    return render(request, 'mysite/webhosting.html', {'plans': data})

def features(request):
    return render(request, 'mysite/features.html')

def about(request):
    return render(request, 'mysite/about.html')

def contact(request):
    return render(request, 'mysite/contact.html')

# @login_required
def order_now(request, price_id):
    data = Price.objects.get(pk=price_id)
    price = data.monthly_price + data.onetime_price
    # if data.monthly_price == price or data.onetime_price == price:
    return render(request, 'mysite/order.html', {'data': data, 'price': price})
