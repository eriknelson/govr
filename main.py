import os, re, json, requests

from subprocess import Popen, PIPE
from os.path import isdir
from os import listdir

# from flask import Flask, request

TEST_SUBSTR = "_test.go"
GITHUB_ROOT = "https://api.github.com"

def merge_d(a, b):
    z = a.copy()
    z.update(b)
    return z

def reduce_line_counts(weights, pkg):
    pkg_name = pkg[0]
    pkg_root = pkg[1]

    find_cmd = ["find", pkg_root, "-name", "*.go"]
    test_filter_cmd = ["grep", "-v", "_test.go"]
    wc_cmd = ["xargs", "wc", "-l"]
    total_cmd = ["grep", "total"]

    find_p = Popen(find_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    test_filter_p = Popen(
        test_filter_cmd, stdin=find_p.stdout,
        stdout=PIPE, stderr=PIPE)
    wc_p = Popen(
        wc_cmd, stdin=test_filter_p.stdout,
        stdout=PIPE, stderr=PIPE)
    total_p = Popen(
        total_cmd, stdin=wc_p.stdout,
        stdout=PIPE, stderr=PIPE)

    output, err = total_p.communicate()

    lines = re.search(r'(\d+) total', output).groups()[0]

    weights[pkg_name] = int(lines)
    return weights

def discount_factors(counts):
    total = float(reduce(
        lambda total, lines: total + lines,
        counts.itervalues(), 0))

    return reduce(lambda weights, (pkg, lines): merge_d(weights, { pkg: {
        "lines": lines, "discount": lines / total
    }}), counts.iteritems(), {})

def pkg_coverage(project_root, pkgs):
    test_cmd = ["go", "test", "./pkg/...", "-cover"]
    test_p = Popen(
        test_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=project_root)
    output, err = test_p.communicate()
    output_a = output.split('\n')[:-1]

    coverage = {}
    for pkg in pkgs:
        thing = os.path.join("pkg", pkg)
        coverage_str = [s for s in output_a
                if os.path.join("pkg", pkg) in s][0]
        regex = pkg + r'.*coverage.* (\d+\.\d)%'
        coverage[pkg] = float(re.search(regex, coverage_str).groups()[0])

    return coverage


def insert_coverage(weights, coverage):
    for pkg, val in coverage.iteritems():
        weights[pkg]["coverage"] = val
        weights[pkg]["discount_coverage"] = val * weights[pkg]["discount"]

def coverage_report(weights, project_coverage):
    report = [
        "============================================================",
        "                      GOVRAGE REPORT                        ",
        "============================================================"
    ]

    report.extend(["[ %s ] -> [ %s%% ]" % (pkg, v["coverage"])
        for (pkg, v) in weights.iteritems()])

    report.extend([
        "Total Coverage: [ %s%% ]" % project_coverage,
        "============================================================"
    ])
    return '\n'.join(report)

# app = Flask(__name__)

# @app.route("/")
# def hello():
    # return "break the hairpin\n"

# @app.route("/hook", methods=['POST'])
# def hook():
    # data = request.json
    # print data
    # return ("", 200)

def main_coverage():
    project_root = os.environ['GOVR_PROJECT_ROOT']
    pkg_root = os.path.join(project_root, "pkg")
    pkgs = [(pkg, os.path.join(pkg_root, pkg)) for pkg in listdir(pkg_root)]
    weights = discount_factors(reduce(reduce_line_counts, pkgs, {}))
    coverage = pkg_coverage(project_root, weights.keys())
    insert_coverage(weights, coverage)
    project_coverage = round(reduce(
        lambda pc, meta: pc + meta["discount_coverage"],
        weights.itervalues(), 0), 2)

    print coverage_report(weights, project_coverage)

    weights["total_coverage"] = project_coverage

    print json.dumps(weights)

def gh_set_status(status, owner, repo, sha):
    # Valid status: pending, success, error, failure
    path = "/repos/%s/%s/statuses/%s" % (owner, repo, sha)
    payload = {"state": status, "context": "Test Coverage", "description": "Coverage passed with 50.06%"}
    url = gh_url(path)
    r = requests.post(url, json=payload, auth=(GITHUB_USER, GITHUB_PASS))
    return r.json()

def gh_zen():
  r = requests.get(github_url("/zen"))
  print "Got response: %s" % r.text

def gh_url(path):
  return "%s%s" % (GITHUB_ROOT, path)

if __name__ == "__main__":
  main_coverage()
