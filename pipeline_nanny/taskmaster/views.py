from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from taskmaster.models import *

def jobgroups(request):
	groups = JobGroup.objects.all()
	paginator = Paginator(groups, 25) # Show 25 job groups per page

	page = request.GET.get('page')
	try:
		groups = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		groups = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		groups = paginator.page(paginator.num_pages)

	return render(request, 'taskmaster/job_groups.html', {"groups": groups})

def kickstart(request):
	'''Creates a bunch of models to mess around with'''

	group = JobGroup.objects.create(name="pizza maker group")
	job1 = group.new_job(name="tony job")
	job2 = group.new_job(name="steve job")
	job3 = group.new_job(name="charlie job")

	return redirect('jobgroups')