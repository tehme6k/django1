import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import context
from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects







# def projects(request):
#     projects, search_query = searchProjects(request)
    
#     page = request.GET.get('page')
#     results = 3
#     paginator = Paginator(projects, results)

#     try:
#         projects = paginator.page(page)
#     except EmptyPage:
#         page = paginator.num_pages
#         projects = paginator.page(page)
#     except:
#         page = 1
#         projects = paginator.page(page)

#     custom_range = range(1,20)


#     context = {'projects': projects, 'search_query':search_query, 'paginator':paginator, 'custom_range':custom_range}
#     return render(request, 'projects/projects.html', context)



def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {'projects': projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)



def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        project.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=project.id )


    context = {'project':project, 'form':form}
    return render(request, 'projects/single-project.html', context)



@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form':form}
    return render(request, "projects/project_form.html", context)



@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(request, "projects/project_form.html", context)



@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    project = Project.objects.get(id=pk)
    context = {'object': project}
    return render(request, 'delete_template.html', context)