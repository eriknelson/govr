import requests
from govr.test_runner import TestRunner

COVERAGE_ENDPOINT = "/coverage"

class Travis:
	def __init__(self, args, config):
		self.args = args
		self.config = config
		self.runner = TestRunner(args.project)

	def run(self):
		print "Travis::run"
		print "============================================================"
		print "Project: %s" % self.args.project
		print "Server: %s" % self.config["govr_server"]
		print "Project Owner: %s" % self.config["project_owner"]
		print "Project Repo: %s" % self.config["project_repo"]
		print "Commit: %s" % self.args.travis_commit
		print "============================================================"

		# TODO: Post pending status

		did_pass_coverage = self._coverage_check()
		print "DID PASS COVERAGE: [ %s ]" % did_pass_coverage

		# TODO: Post pass/fail status
		# TODO: Post details with link to logs and the coverage reports

	def _coverage_check(self):
		weights = self.runner.run()
		new_total_coverage = weights["total_coverage"]
		current_coverage = self._(load_current_coverage()

		return new_total_coverage >= current_coverage

	def _load_current_coverage(self):
		# TODO: Something can totally blow up here. Deal with it. At least check
		# status code. Need a broader error handling strat.
		coverage_url = "http://%s%s" % (self.config["govr_server"], COVERAGE_ENDPOINT)
		return requests.get(coverage_url).json()["total_coverage"]
