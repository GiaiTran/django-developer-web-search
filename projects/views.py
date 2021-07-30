from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Project
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .ultils import searchProjects, paginatorProjects

# Create your views here.


def projects(request):

    # topSkills = profile.skill_set.exclude(description__exact="")
    # print(projects)
    results = 3
    projects, search_query = searchProjects(request)
    custom_range, projects = paginatorProjects(request, projects, results)
    context = {
        "projects": projects,
        "search_query": search_query,
        "paginator": paginator,
        "custom_range": custom_range,
    }
    # return render(request, 'projects/projects.html', context)
    return render(request, "projects/projects.html", context)
    # return HttpResponse("TEST")


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    tag = projectObj.tags.all()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()

            projectObj.getVoteCount
            messages.success(request, "Your review was succesfully sumitted!")
            return redirect("project", pk=projectObj.id)

    return render(
        request,
        "projects/single-project.html",
        {"project": projectObj, "tags": tag, "form": form},
    )


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("account")

    context = {"object": project}
    return render(request, "delete_template.html", context)
