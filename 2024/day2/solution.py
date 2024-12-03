from collections import Counter

data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

with open("input.txt") as f:
  data = f.read()

reports = []
for line in data.splitlines():
  reports.append(list(map(int,line.strip().split())))


def isReportSafe(report: list[int]) -> bool: 
  if len(report) < 2:
    return True
  ascending = report[1] > report[0]
  previousLevel = report[0]
  for i in range(1, len(report)):
    difference = report[i] - previousLevel
    previousLevel = report[i]
    if abs(difference) > 3 or difference == 0:
      return False
    if ascending and difference < 0:
      return False
    if not ascending and difference > 0:
        return False

  return True

def isDampenedReportSave(report: list[int]) -> bool:
  if isReportSafe(report):
    return True
  for i in range(len(report)):
    dampenedReport = report[0:i] + report[i+1:]
    if isReportSafe(dampenedReport):
      return True
  return False

safeReports = sum(1 if isReportSafe(report) else 0 for report in reports)
print("Part 1 solution is ", safeReports)

dampenedSafeReports = sum(1 if isDampenedReportSave(report) else 0 for report in reports)
print("Part 2 solution is ", dampenedSafeReports)