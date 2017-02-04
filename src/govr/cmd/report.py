from govr.test_runner import TestRunner

def coverage_report(weights):
	report = [
		"============================================================",
		"                      GOVRAGE REPORT                        ",
		"============================================================"
	]

	report.extend(["[ %s ] -> [ %s%% ]" % (pkg, v["coverage"])
		for (pkg, v) in weights.iteritems() if pkg != "total_coverage"])

	report.extend([
		"Total Coverage: [ %s%% ]" % weights["total_coverage"],
		"============================================================"
	])
	return '\n'.join(report)

class Report:
	def __init__(self, args):
		self.project = args.project
		self.runner = TestRunner(self.project)

	def run(self):
		weights = self.runner.run()
		return coverage_report(weights)
