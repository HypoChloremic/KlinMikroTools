from analysis_script import KlinMikroTools

run = KlinMikroTools()

xl, sheetnames = run.load_excel("qlikview_fryslista_union.xlsx")
keys, allData     = run.load_data_excel(xl, "Sheet3", True)
allAP = run.fix_AP(allData, 0, 2)



for sheet in sheetnames:
	keys, data 	   = run.load_data_excel(xl, sheet, True)
	newData = []

	for i in data:
		for ind, k in enumerate(allAP):
			if i[1] in k:
				newData.append(i)
				for u in allData[ind]:
					newData[-1].append(u)

	run.config["OUTPUT_CSV"] = f"{sheet}.csv"
	st = run.gen_csv(newData)
	run.save_csv(st)









