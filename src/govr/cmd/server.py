from flask import Flask, request

from os import path, makedirs

class Server:
	FLASK_APP_NAME = "govrd"

	def __init__(self, args):
		self.host = args.server_host
		self.port = args.server_port
		self.debug = args.server_debug
		self.state_dir = args.server_state_dir
		self.app = Flask(Server.FLASK_APP_NAME)

		self.app.add_url_rule("/", methods=["GET"], view_func=self.hello)
		self.app.add_url_rule("/coverage", methods=["GET"], view_func=self.coverage)

		if not os.path.exists(self.state_dir):
			os.makedirs(self.state_dir)

	def hello(self):
		return "Break the hairpin\n"

	def hook(self):
		data = request.json
		return ("", 200)

	def coverage(self):
		print "coverage"

	def run(self):
		self.app.run(
			debug=self.debug,
			host=self.host,
			port=int(self.port)
		)
