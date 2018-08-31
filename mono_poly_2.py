from analysis_script import KlinMikroTools

run = KlinMikroTools()
xl, sheetnames = run.load_excel("1518_qlikview_an.xlsx")
keys, data = run.load_data_excel(xl, "Sheet1", True)
AP = run.fix_AP(data, 0, 2)
AP = [i[0] for i in AP]

xl2, sheetnames = run.load_excel("1518_qlikview_an.xlsx")
keys2, data2    = run.load_data_excel(xl2, "Sheet1", True) 
AP2 = [i[1] for i in data2]

ttan = "Tid till detektion i anaerobflaskan"
ttae = "Tid till detektion i aerobflaskan"

age     = [i[-3] for i in data]
ankomst = [i[6] for i in data]
n = 0
k = 0
b = 0
d = {}

newdict = {i:[0, []] for i in AP}

for ind, i in enumerate(AP):
	if not data[ind][11] in newdict[i][-1] :
		newdict[i][0] += 1
		newdict[i][-1].append(data[ind][11])

for i in newdict.keys():
	if newdict[i][0] < 2:
		n    += 1
		d[i] = newdict[i]
	elif newdict[i][0] > 1:
		k += 1
		b += len(newdict[i][-1])

for key,i in zip(d.keys(), d.values()):
	print(key, i)

print(len(AP), n, k, b)






