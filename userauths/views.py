from django.shortcuts import redirect, render
from userauths.forms import UserRgisterForm
from django.contrib.auth import login, authenticate , logout  # Ajout de la fonction authenticate
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL



def register_view(request):
    if request.method == "POST":
        form = UserRgisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created successfully")

            # Use form.cleaned_data['email'] instead of form.cleaned_data['username']
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            
            login(request, new_user)
            return redirect("ecommerce:index")
    else:
        form = UserRgisterForm()
    
    
    
    

    context = {'form': form}
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("ecommerce:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user  = User.object.get(email = email)
    
        except:
            messages.warning(request, f"User with {email} does not exist.")
        
        
        user = authenticate(request,  email = email, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in.")
            return redirect("ecommerce:index")
        
        else:
            messages.warning(request, "User does not exist. Create an account.")


    context = {

    }
    
    return render(request, "userauths/sign-in.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")
