import requests

GITHUB_ROOT = "https://api.github.com"

class Client:
	def __init__(self, user, password):
		self.user = user
		self.password = password

	def set_status(self, status, owner, repo, sha):
		# Valid status: pending, success, error, failure
		path = "/repos/%s/%s/statuses/%s" % (owner, repo, sha)
		payload = {"state": status, "context": "Test Coverage", "description": "Coverage passed with 50.06%"}
		url = gen_url(path)
		r = requests.post(url, json=payload, auth=(self.user, self.password))
		return r.json()

	def zen(self):
		r = requests.get(gen_url("/zen"))
		print "Got response: %s" % r.text

def gen_url( path):
	return "%s%s" % (GITHUB_ROOT, path)
