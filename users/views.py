from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# from django.contrib.auth.forms import UserCreationForm
from .ultils import searchProfiles, paginatorProfiles
from django.contrib import messages
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm


def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":

        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            # print("Username does not exist.")
            messages.error(request, "Username does not exist.")

        # Perform authentication the user with username and password
        user = authenticate(request, username=username, password=password)

        # if the user is existed, we'll create a session and store it in
        # user browswer.
        if user is not None:
            login(request, user)
            return redirect(
                request.GET.get("next") if "next" in request.GET else "account"
            )
        else:
            messages.error(request, "Username or password is incorrect.")
            # print("Username or password is incorrect.")

        # print(username, password)
    return render(request, "users/login_register.html", {"page": page})


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect("login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")

            login(request, user)
            return redirect("edit-account")

        else:
            messages.error(request, "An error has been occurred during registration.")

    context = {"page": page, "form": form}

    # page = 'register'
    return render(request, "users/login_register.html", context)


# Create your views here.
def profiles(request):
    results = 3
    profiles, search_query = searchProfiles(request)
    # profiles = (
    #     Profile.objects.exclude(name__isnull=True)
    #     .exclude(bio__isnull=True)
    #     .exclude(short_intro__exact="")
    # )
    custom_range, profiles = paginatorProfiles(request, profiles, results)
    context = {
        "profiles": profiles,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "users/profiles.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    # projects = profile.project_set.all()

    context = {
        "profile": profile,
        "topSkills": topSkills,
        "otherSkills": otherSkills,
        # "projects": projects,
    }

    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    # topSkills = profile.skill_set.exclude(description__exact="")
    topSkills = profile.skill_set.all()
    # print(topSkills)
    projects = profile.project_set.all()
    context = {"profile": profile, "topSkills": topSkills, "projects": projects}

    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def createSkill(request):
    form = SkillForm()
    profile = request.user.profile
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.onwer = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")

    context = {"form": form}
    print(form)
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            # skill = form.save(commit=False)
            # skill.onwer = profile
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def deleteSkill(request, pk):
    # profile = request.user.profile
    # project = profile.project_set.get(id=pk)

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect("account")
    context = {"object": skill}
    # context = {}
    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unreadCount": unreadCount}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()
    # messageRequests = profile.messages.all()
    # unreadCount = messageRequests.filter(is_read=False).count()
    context = {"message": message}
    return render(request, "users/message.html", context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    # If the user is not authenticated, set sender to None
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            # Store name and email if user is authenticated
            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect("user-profile", pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)
