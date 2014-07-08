from django.test import TestCase
from taskmaster.models import *

class DependencyTestCase(TestCase):
	def setUp(self):
		self.group = JobGroup.objects.create(name="pizza maker group")
		self.job1 = self.group.new_job(name="tony job")
		self.job2 = self.group.new_job(name="steve job")
		self.job3 = self.group.new_job(name="charlie job")

	def test_adding_self(self):
		"""Jobs can't be self-dependent"""
		j1, j2, j3 = self.job1, self.job2, self.job3

		self.assertRaises(InvalidDependencyException, lambda: j1.add_parent(j1))
		self.assertRaises(InvalidDependencyException, lambda: j1.add_child(j1))

		j1.add_child(j2)
		j2.add_child(j3)

		self.assertRaises(InvalidDependencyException, lambda: j3.add_child(j1))

	def test_depends_on(self):
		"""The depends_on method can follow relationships"""
		j1, j2, j3 = self.job1, self.job2, self.job3

		self.assertFalse(j2.depends_on(j1), "simple dependency not added yet is ignored")

		j1.add_child(j2)
		j2.add_child(j3)

		self.assertTrue(j2.depends_on(j1), "simple dependency detected")
		self.assertFalse(j1.depends_on(j2), "simple reverse-dependency ignored")

		self.assertTrue(j3.depends_on(j1), "extended dependency detected")
		self.assertFalse(j1.depends_on(j3), "extended reverse-dependency ignored")

		self.assertFalse(j1.depends_on(j1), "no self dependency exists")

	def test_status_transitions(self):
		"""Job statuses are updated properly when adding parents"""
		j1, j2, j3 = self.job1, self.job2, self.job3

		self.assertEqual(j1.status, Job.READY, "Free-floating job is Ready")
		self.assertEqual(j2.status, Job.READY, "Other free-floating job is Ready")

		j1.add_child(j2)

		self.assertEqual(j1.status, Job.READY, "Parent job is Ready")
		self.assertEqual(j2.status, Job.WAITING, "Child job is waiting")

	# def test_status_refuses_adding_dependencies(self):
	# 	"""Depndencies can't be added unless a job is in the Ready or Waiting state"""
	# 	j1, j2, j3 = self.job1, self.job2, self.job3

	# 	self.assertEquals(j1.status, Job.READY)

	# 	j1.add_child(j2)
	# 	j2.add_child(j3)

	# 	self.assertTrue(j2.depends_on(j1), "simple dependency detected")
	# 	self.assertFalse(j1.depends_on(j2), "simple reverse-dependency ignored")

	# 	self.assertTrue(j3.depends_on(j1), "extended dependency detected")
	# 	self.assertFalse(j1.depends_on(j3), "extended reverse-dependency ignored")

	# 	self.assertFalse(j1.depends_on(j1), "no self dependency exists")

	# def test_refuse_adding_children_to_completed_jobs(self):
	# 	"""Child jobs can't be added to jobs that have already completed"""