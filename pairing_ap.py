## Pairing AP numbers 
from analysis_script import KlinMikroTools

xl, sheetnames = run.load_excel("2015_2018_all.xls")
keys, frysdata = run.load_data_excel(xl, "15_18_frys_all", nativeList = True)

xl, sheetnames = run.load_excel("2015_2018_all.xls")
keys, allData  = run.load_data_excel(xl, "Main", nativeList = True)


allAp = run.fix_AP(allData, 0, 2)

allAp = [i[0] for i in allAp]
AP = [i[3] for i in frysdata]

newData = []

for ind,i in enumerate(AP):
	for ind2, k in enumerate(allAp):
		try:
			if k in i:
				newData.append(frysdata[ind])
				for z in allData[ind2]:
					newData[-1].append(z)
		except TypeError as e:
			pass

st = run.gen_csv(newData)
run.save_csv(st)