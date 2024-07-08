from django.http import HttpResponse
from django.shortcuts import render
from user.models import ProfileEmployeur
from post.models import Category, Job
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
# from visits.models import Visits
# Create your views here.
def homePage(request):
    category = Category.objects.all()
    job = Job.objects.all()

    context = {
        'job':job,
        'category':category,
    }

    return render(request, 'index.html',context)

def jobPage(request):
    category = Category.objects.all()
    job = Job.objects.all()

    context = {
        'job':job,
        'category':category,
    }
    return render(request, 'job.html',context)

def jobSearch(request):
    job_title = request.GET['title']
    locality = request.GET['location']
    job = Job.objects.filter(title__icontains = job_title)

    context = {
        'job':job,
        'job_title':job_title,
        'locality':locality,
    }
    return render(request, 'jobSearchPage.html', context)

def categoryPage(request):
    category = Category.objects.all()

    context = {
        'category':category,
    }
    return render(request, 'category.html',context)

def categoryJobPage(request, cid):
    cat = Category.objects.get(cid = cid)
    job = Job.objects.filter(category=cat)

    context = {
        'job':job,
        'cat':cat
    }
    return render(request, 'category-job.html', context)


def jobDetail(request, jid):
    job = Job.objects.get(jid=jid)
    context = {
        'job':job
    }
    return render(request, 'job-detail.html', context)

def contactUs(request):
    return render(request, 'contact.html')


@login_required(login_url='/auth/sign-in/')
def adminJobList(request):
    job = Job.objects.filter(author=ProfileEmployeur.objects.get(user=request.user))

    context={
        'job':job
    }
    return render(request, 'adminJobList.html', context)


@login_required(login_url='/auth/sign-in/')
def addjob(request):
    cat = Category.objects.all()

    context = {
        'cat':cat
    }
    return render(request, 'addjobalert.html', context)