import json

from flask import Flask, request, jsonify
from os import path, makedirs
from subprocess import Popen, PIPE
from govr.util import is_dir_empty
from govr.test_runner import TestRunner
from govr.shields import update_shield

PROJECT_DIR_NAME = "project"
IMG_DIR_NAME = "img"
REPORTS_DIR_NAME = "reports"
COVERAGE_FILE = "coverage.json"

def routes(server):
	server.app.add_url_rule("/", methods=["GET"], view_func=server.hello)
	server.app.add_url_rule("/coverage", methods=["GET"], view_func=server.coverage)
	server.app.add_url_rule("/hook", methods=["POST"], view_func=server.hook)

class Server:
	FLASK_APP_NAME = "govr-server"

	def __init__(self, args):
		if args.server_git_repo == "":
			raise Exception("Cannot run server without clonable git repo url, via --server-git-repo=$REPO")
		self.git_repo = args.server_git_repo

		self.host = args.server_host
		self.port = args.server_port
		self.debug = args.server_debug
		self.state_dir = args.server_state_dir
		self.coverage_file = path.join(self.state_dir, COVERAGE_FILE)
		self.app = Flask(Server.FLASK_APP_NAME)

		self.state_dirs = self._init_state_dirs()
		checkout_project(self.git_repo, self.state_dirs[PROJECT_DIR_NAME])
		self.test_runner = TestRunner(self.state_dirs[PROJECT_DIR_NAME])

		# TODO: Checkout alternative branch to master if configured? Not impl yet.

		self._init_coverage_file()
		update_shield(self.state_dirs[IMG_DIR_NAME], self._read_total_coverage())

		routes(self)

	######################################################################
	# ROUTE HANDLERS
	######################################################################
	def hello(self):
		return "Break the hairpin\n"

	def coverage(self):
		return jsonify({"total_coverage": self._read_total_coverage()})

	def hook(self):
		# TODO: Queue? Concurrant runs? Make sure most recent push is triggering?

		new_master_push = \
			request.json["ref"] == "refs/heads/master" and \
			request.headers["X-Github-Event"] == "push"

		# Pull
		test_sha = request.json["after"]
		self._update_project(test_sha)

		# If it's not a push even we care about, ignore
		if not new_master_push:
			return ("", 200)

		self._update_coverage()
		update_shield(self.state_dirs[IMG_DIR_NAME], self._read_total_coverage())

		return ("Running update", 202)
	######################################################################

	def run(self):
		self.app.run(
			debug=self.debug,
			host=self.host,
			port=int(self.port)
		)

	def _init_state_dirs(self):
		ret = {}
		if not path.exists(self.state_dir):
			makedirs(self.state_dir)

		state_dirs = [PROJECT_DIR_NAME, IMG_DIR_NAME, REPORTS_DIR_NAME]
		for state_dir, full_state_dir in [(dd, path.join(self.state_dir, dd)) for dd in state_dirs]:
			if not path.exists(full_state_dir):
				makedirs(full_state_dir)
			ret[state_dir] = full_state_dir

		return ret

	def _init_coverage_file(self, overwrite=True):
		if path.exists(self.coverage_file) and not overwrite:
			return

		self._update_coverage()

	def _update_project(self, sha):
		# TODO: Handle errors on these cmds
		fetch_cmd = ["git", "fetch", "--all", ]
		checkout_cmd = ["git", "checkout", sha]

		fetch_p = Popen(fetch_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE,
			cwd=self.state_dirs[PROJECT_DIR_NAME])
		output, error = fetch_p.communicate()

		checkout_p = Popen(checkout_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE,
			cwd=self.state_dirs[PROJECT_DIR_NAME])
		output, error = checkout_p.communicate()

	def _update_coverage(self):
		coverage = self.test_runner.run()

		print "Writing coverage to file: %s" % self.coverage_file
		with open(self.coverage_file, "w") as coverage_file:
				coverage_file.write(json.dumps(coverage))

	def _read_total_coverage(self):
		with open(self.coverage_file) as coverage_file:
			# TODO: Error handling?
			weights = json.load(coverage_file)
			return weights["total_coverage"]

def checkout_project(clone_url, path):
	if is_dir_empty(path):
		print "Cloning [ %s ] to [ %s ]" % (clone_url, path)
		clone_cmd = ["git", "clone", clone_url, path]

		clone_p = Popen(clone_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = clone_p.communicate()
		print output
