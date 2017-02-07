from hashlib import md5
from subprocess import Popen, PIPE
from os import path

SHIELDS_ROOT = "https://img.shields.io/badge"
SHIELD_TEXT = "coverage"
LATEST_SVG = "latest-shield.svg"

# match on  range[i][1] > coverage >= range[i][0]

RANGES = [
	(0.0, 10.0, "red"),
	(10.0, 20.0, "orage"),
	(30.0, 40.0, "yellow"),
	(40.0, 50.0, "yellowgreen"),
	(50.0, 60.0, "green"),
	(60.0, 100.0, "brightgreen"),
]

def get_color(coverage):
	if coverage <= 0.0: return "red"

	color = None
	for color_range in RANGES:
		if coverage >= color_range[0] and coverage < color_range[1]:
			color = color_range[2]
			break

	if not color: color = "red"
	return color

def gen_shield_file(url):
	return "%s.svg" % md5(url).hexdigest()

def gen_shield_url(coverage, color):
	return "%s/%s-%s%%-%s.svg" % (SHIELDS_ROOT, SHIELD_TEXT, coverage, color)

def link_shield(img_dir, src_file):
	dest_link = path.join(img_dir, LATEST_SVG)
	relative_src = "./%s" % src_file
	ln_cmd = ["ln", "-sf", relative_src, dest_link]
	ln_p = Popen(ln_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = ln_p.communicate()
	print output

def download_shield(url, file_name, img_dir):
	full_file = path.join(img_dir, file_name)
	wget_cmd = ["wget", "-O", full_file, url]
	wget_p = Popen(wget_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = wget_p.communicate()
	print output

def update_shield(img_dir, coverage):
	color = get_color(coverage)
	url = gen_shield_url(coverage, color)
	shield_file = gen_shield_file(url)
	full_shield_file = path.join(img_dir, shield_file)

	# Check if shield is already cached
	if not path.exists(full_shield_file):
		download_shield(url, shield_file, img_dir)

	link_shield(img_dir, shield_file)
