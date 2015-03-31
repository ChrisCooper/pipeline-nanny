from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from taskmaster.models import *

def jobgroups(request):
	groups = JobGroup.objects.all().order_by('-date_created')
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

def jobgroup(request, group_id):
	group = get_object_or_404(JobGroup, id=group_id)
	return render(request, 'taskmaster/job_group.html', {"group": group})


def kickstart(request):
	'''Creates a bunch of models to mess around with'''

	group = JobGroup.objects.create(name="Hawaiian pizza")
	job1 = group.new_job(name="base job")
	job2 = group.new_job(name="pineapple job")
	job3 = group.new_job(name="ham job")
	job4 = group.new_job(name="cheese job")

	job1.add_children([job2, job3])
	job4.add_parents([job2, job3])

	return redirect('jobgroups')