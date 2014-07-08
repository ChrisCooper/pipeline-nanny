from django.shortcuts import render, get_object_or_404
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