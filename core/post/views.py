from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from user.models import ProfileEmployeur
from post.models import Category, Job
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib import messages
from taggit.models import Tag
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

    # url = request.META.get('HTTP_REFERER')
    cat = Category.objects.all()
    if request.method == 'POST' :
        job_title = request.POST['title']
        category = request.POST['category']
        description = request.POST['description']
        requiements = request.POST['requiements']
        responsability = request.POST['responsability']
        experience = request.POST['experience']
        salary = request.POST['salary']
        type = request.POST['type']
        conpetence = request.POST.getlist('conpetence')
        tags_l = request.POST.getlist('tags')
        diplomes = request.POST['diplomes']
        genre = request.POST['genre']
        locality = request.POST.getlist('locality')
        expiration = request.POST['expiration']
        image = request.POST['image']
        email = request.POST['email']
        whatsapp = request.POST['whatsapp']
        phone = request.POST['phone']
        linkedin = request.POST['linkedin']
        twitter = request.POST['twitter']
        instagram = request.POST['instagram']
        facebook = request.POST['facebook']
        youtube = request.POST['youtube']
        

        # Conversion en objet datetime
        date_obj = datetime.strptime(expiration, "%A %d %B %Y - %H:%M")

        # Conversion en format compatible Django
        expiration = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        category_inst = Category.objects.get(title = category)
                    
        new_job = Job.objects.create(
            author = ProfileEmployeur.objects.get(user=request.user),
            title = job_title,
            image = image,
            category = category_inst,
            description = description,
            requierements = requiements,
            responsability = responsability,
            experience =experience,
            salary = salary,
            type = type,
            qualification = diplomes,
            genre = genre,
            expire_date =expiration,
            facebook_link = facebook,
            instagram_link = instagram,
            twetter_link = twitter,
            youtube_link = youtube,
            mail =email,
            phone =phone,
            whatsapp =whatsapp
        )
    
        if conpetence:
            for c in conpetence:
               new_job.competence.add(c)

        # Ajouter des tags
        if tags_l:
            for tag in tags_l:
               new_job.tag.add(tag)
             
    context = {
        'cat':cat,
    }
    return render(request, 'addjobalert.html', context)

