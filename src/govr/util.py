import os

def merge_d(a, b):
	z = a.copy()
	z.update(b)
	return z

def is_dir_empty(path):
	return os.listdir(path) == []
