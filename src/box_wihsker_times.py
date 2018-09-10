import matplotlib.pyplot as plt
from analysis_script import KlinMikroTools
import datetime


xl, sheetnames = run.load_excel("official_work_environ.xlsx")
keys, data = run.load_data_excel(xl, "BX_RES_15_18_1030_POS", True)

data   = run.load_data_csv("some_other.csv")
times  = [i[-2].split(":") for i in data[1:]]
times2 = []

for i in times:
	times2.append([])
	for k in i:
		try: times2[-1].append(int(k))
		except ValueError as e: pass

hours = []
for i in times2:
	try:
		st = i[0]*24 + i[1] + (i[2]/60)
		hours.append(st)
	except IndexError as e:
		pass
