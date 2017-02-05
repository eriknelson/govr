import os, yaml

def load_config(path):
	with open(path, "r") as config:
		return yaml.load(config)

def merge_d(a, b):
	z = a.copy()
	z.update(b)
	return z

def is_dir_empty(path):
	return os.listdir(path) == []
