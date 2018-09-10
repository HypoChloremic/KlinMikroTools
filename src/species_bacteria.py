from analysis_script import KlinMikroTools

with open("bakt.txt", "r") as file:
	bakt = file.readlines()
	bakt = [i.replace("\n", "") for i in bakt]
	bakt = [i.split(":") for i in bakt]

run = KlinMikroTools()
xl, sheetnames = run.load_excel("1518_anaerobes.xlsx")
keys, allData  = run.load_data_excel(xl, "an_bot_sheet", True)
allAP = run.fix_AP(allData, 0, 2)
selectDict = {"bacteroides": "bacteroides spp", "clostridium": "clostridium spp", 
"actinotignum": "actinobaculum spp", "actinobaculum": "actinobaculum spp", 
"fusobacterium":"fusobacterium spp", "actinomyces":"actinomyces spp"}

newData = []

for i in allData:
	newData.append(i)
	for k in bakt:
		if k[0] in i[11].lower():
			newData[-1].append(k[-1])
			for u in selectDict.keys():
				try:
					newData[-1][11] = selectDict[k[0]] 
					
				except IndexError as e:
					pass
				except KeyError as e: 
					pass

run.config["OUTPUT_CSV"] = "1518_anaerobes.csv"
st = run.gen_csv(newData)
run.save_csv(st)
