#!/usr/bin/env python
import os, re, json, argparse

from govr.cmd import *

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("project", help="Project under test")

	parser.add_argument("-r", "--report",
		help="Prints coverage report", action="store_true")

	parser.add_argument("-t", "--travis",
		help="Run as client under travis ci", action="store_true")

	parser.add_argument("-s", "--server",
		help="Run as server", action="store_true")
	parser.add_argument("--server-host",
		help="Host to run flask server on", default="127.0.0.1")
	parser.add_argument("--server-port",
		help="Port to run flask server on", default=1337)
	parser.add_argument("--server-debug",
		help="Run server in debug mode", action="store_true")
	parser.add_argument("--server-state-dir",
		help="File where runtime state is stored", default="/var/lib/govr")

	args = parser.parse_args()

	print "Running against project: %s" % args.project

	if args.travis:
		Travis(args).run()
	elif args.server:
		"Running server"
		Server(args).run()
	else:
		print Report(args).run()
