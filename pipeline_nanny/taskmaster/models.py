from django.db import models

class JobGroup(models.Model):
	name = models.TextField()
	date_Created = models.DateTimeField('date created', auto_now_add=True)

	def new_job(self, **args):
		return Job.objects.create(group=self, **args)

	def __repr__(self):
		return "<Job group: (" + ", ".join(self.jobs) + ")>"

	#def ready_jobs(self):
		#return self.jobs.

class Job(models.Model):
	name = models.TextField()
	group = models.ForeignKey('JobGroup', related_name='jobs')
	child_jobs = models.ManyToManyField('self', symmetrical=False, related_name='parent_jobs')

	WAITING = 0
	READY = 1
	RUNNING = 2
	COMPLETED = 3
	ERRORED = 4
	KILLED = 5
	STATUSES = (
		(WAITING, 'Waiting'), # waiting on parent jobs
		(READY, 'Ready'), # Can be started any time
		(RUNNING, 'Running'), # Has been started
		(COMPLETED, 'Completed'), # Exited with zero code
		(ERRORED, 'Errored-out'), # Exited with a non-zero status
		(KILLED, 'Killed'), # Used too many resources and was killed
	)
	status = models.IntegerField(choices=STATUSES, default=READY)
   
	def __repr__(self):
		return "<{status} Job: {name}, {n_parents} parents, {n_children} children>".format(
			status=self.get_status_display(),
			name=self.name,
			n_parents=self.parent_jobs.count(),
			n_children=self.child_jobs.count())
	
	def add_child(self, dependant_job):
		if dependant_job == self:
			raise InvalidDependencyException("Error: Can't add a job as its own child. Job is {0}".format(self))
		if self.depends_on(dependant_job):
			raise InvalidDependencyException("Error: Dependency loops are not allowed. {0} already depends on {1}".format(self, dependant_job))
		if dependant_job in self.child_jobs.all():
			raise InvalidDependencyException("Error: Child job has already been added. {1} already depends on {0}".format(self, dependant_job))
		if self.status not in (Job.READY, Job.WAITING):
			raise InvalidDependencyException("Error: Can't add a child to a parent job that's already started. {0} already running (child: {1})".format(self, dependant_job))
		if dependant_job.status not in (Job.READY, Job.WAITING):
			raise InvalidDependencyException("Error: Can't add a child job that's already started. {1} already running (parent: {0})".format(self, dependant_job))
	   
		self.child_jobs.add(dependant_job)
		dependant_job.status = Job.WAITING

	def add_parent(self, prerequisite_job):
		prerequisite_job.add_child(self)

	def add_parents(self, prerequisite_jobs):
		for job in prerequisite_jobs:
			self.add_parent(job)

	def add_children(self, dependent_jobs):
		for job in dependent_jobs:
			self.add_child(job)
   
	def depends_on(self, job):
		if (job in self.parent_jobs.all()):
			return True
	   
		for dependency in self.parent_jobs.all():
			if dependency.depends_on(job):
				return True
		return False

class InvalidDependencyException(Exception):
	pass
