from django.db import models

class JobGroup(models.Model):
	name = models.TextField()
	date_Created = models.DateTimeField('date created')

	def __repr__(self):
		return "Job group: (" + ", ".join(self.jobs) + ")"

class Job(object):
	name = models.TextField()
	group = models.ForeignKey('JobGroup')
	child_jobs = models.ManyToManyField('self', symmetrical=False, related_name='parent_jobs')
   
	def __repr__(self):
		return "<Job: {0}, {1} parents, {2} children>".format(self.name, self.parent_jobs.count(), self.child_jobs.count())
	
	def add_child(self, dependant_job):
		if dependant_job == self:
			raise Exception("Error: Can't add a job as its own child. Job is {0}".format(self))
		if self.depends_on(dependant_job):
			raise Exception("Error: Dependency loops are not allowed. {0} already depends on {1}".format(self, dependant_job))
		if dependant_job in self.child_jobs:
			raise Exception("Error: Child job has already been added. {0} already depends on {1}".format(dependant_job, self))
	   
		self.child_jobs.add(dependant_job)

	def add_parent(self, prerequisite_job):
		if prerequisite_job == self:
			raise Exception("Error: Can't add a job as its own parent. Job is {0}".format(self))
		if prerequisite_job.depends_on(self):
			raise Exception("Error: Dependency loops are not allowed. {0} already depends on {1}".format(prerequisite_job, self))
		if prerequisite_job in self.parent_jobs:
			raise Exception("Error: Parent job has already been added. {0} already depends on {1}".format(self, prerequisite_job))
	   
		self.parent_jobs.add(prerequisite_job)

	def add_parents(self, prerequisite_jobs):
		for job in prerequisite_jobs:
			self.add_parent(job)

	def add_children(self, dependent_jobs):
		for job in dependent_jobs:
			self.add_child(job)
   
	def depends_on(self, job):
		if (job in self.parent_jobs):
			return True
	   
		for dependency in self.parent_jobs:
			if dependency.depends_on(job):
				return True
		return False


