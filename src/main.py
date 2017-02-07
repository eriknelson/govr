#!/usr/bin/env python
import os, argparse

from govr.cmd import *
from govr.util import load_config

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_TRAVIS_CONFIG_FILE = "govr-travis.yml"
DEFAULT_TRAVIS_CONFIG = os.path.join(MAIN_DIR, DEFAULT_TRAVIS_CONFIG_FILE)

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument("-r", "--report",
		help="Prints coverage report", action="store_true")

	parser.add_argument("-t", "--travis",
		help="Run as client under travis ci", action="store_true")
	parser.add_argument("--travis-config", help="travis mode configuration file",
		default=DEFAULT_TRAVIS_CONFIG)
	parser.add_argument("--travis-commit", help="Commit sha under test")

	parser.add_argument("--project",
			help="Project path under test, required by -r and -t")

	parser.add_argument("-s", "--server",
		help="Run as server", action="store_true")
	parser.add_argument("--server-host",
		help="Host to run flask server on", default="127.0.0.1")
	parser.add_argument("--server-port",
		help="Port to run flask server on", default=8080)
	parser.add_argument("--server-debug",
		help="Run server in debug mode", action="store_true")
	parser.add_argument("--server-state-dir",
		help="File where runtime state is stored", default="/var/lib/govr")
	parser.add_argument("--server-git-repo",
		help="Clonable git path to repo under test", default="")

	args = parser.parse_args()

	print "Running against project: %s" % args.project

	if args.travis:
		if not args.project:
			raise Exception("ERROR: Must provide a valid govr-travis.yml configuration via --travis-config")
		if not args.travis_config:
			raise Exception("ERROR: Must provide a valid govr-travis.yml configuration via --travis-config")
		if not args.travis_commit:
			raise Exception("ERROR: Must provide commit sha under test for status updates")

		Travis(args, load_config(args.travis_config)).run()
	elif args.server:
		"Running server"
		Server(args).run()
	else:
		if args.project == "":
			raise Exception("ERROR: Running in report mode requires a --project path to test")
		print Report(args).run()

if __name__ == "__main__":
	main()
