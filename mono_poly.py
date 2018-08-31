from analysis_script import KlinMikroTools

run = KlinMikroTools()
xl, sheetnames = run.load_excel("1518_qlikview_an.xlsx")


keys, data = run.load_data_excel(xl, "Sheet1", True)
AP = run.fix_AP(data, 0, 2)
AP = [i[0] for i in AP]

xl2, sheetnames = run.load_excel("1518_qlikview_an.xlsx")
keys2, data2    = run.load_data_excel(xl2, "Sheet1", True) 
AP2 = [i[1] for i in data2]

age = [i[-3] for i in data]
ankomst = [i[6] for i in data]

newdict = {i:[0, []] for i in AP}

for ind, i in enumerate(AP):
	if i in newdict: 
		if not data[ind][11] in newdict[i][-1]:
			newdict[i][0] += 1
			newdict[i][-1].append(data[ind][11])

n = 0
d = {}
for i in newdict.keys():
	if newdict[i][0] > 1:
		n    += 1
		d[i] = newdict[i]


for key,i in zip(d.keys(), d.values()):
	print(key, i)

print(n)