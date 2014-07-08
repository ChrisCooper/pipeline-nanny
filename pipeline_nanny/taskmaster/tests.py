from django.test import TestCase
from taskmaster.models import *

class DependencyTestCase(TestCase):
	def setUp(self):
		self.group = JobGroup.objects.create(name="pizza maker group")
		self.job1 = self.group.new_job(name="tony job")
		self.job2 = self.group.new_job(name="steve job")

	def test_adding_self(self):
		"""Jobs can't be self-dependent"""
		j = self.job1
		with self.assertRaises(InvalidDependencyException):
			j.add_parent(j)

		with self.assertRaises(InvalidDependencyException):
			j.add_child(j)