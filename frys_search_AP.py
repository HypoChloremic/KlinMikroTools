from analysis_script import KlinMikroTools

run = KlinMikroTools()

AP = run.load_data_csv("Hello_searchres2.csv")
AP = [i[0] for i in AP]


frysfiler = ["Fryslista_AP_2015_VO.xlsx",
					"Fryslista_AP_2016_VO.xlsx",
					"Fryslista_AP_2017_VO.xlsx",
					"Fryslista_AP_2018_VO.xlsx"]

offData = []
for fil in frysfiler:
		xl, sheetnames = run.load_excel(fil)
		for sheet in sheetnames:
			keys, data = run.load_data_excel(xl, sheet, True)
			for ap in AP:
				for u in data:
					for k in u:
						try:
							if ap in k:
								offData.append(u)
						except Exception as e:
							pass


print(len(offData))