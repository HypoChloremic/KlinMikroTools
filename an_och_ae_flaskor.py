from analysis_script import KlinMikroTools

run = KlinMikroTools()
xl, sheetnames = run.load_excel("1518_qlikview_an.xlsx")
keys, data = run.load_data_excel(xl, "Sheet1", True)
AP = run.fix_AP(data, 0, 2)
AP = [i[0] for i in AP]

ttan = "anaerobflaska"
ttae = "aerobflaska"

with open("scripts\\notinaer.txt", "r") as file:
	baktana = file.readlines()
	baktana = [i.replace("\n", "") for i in baktana]

with open("scripts\\caninaer.txt", "r") as file:
	baktaer = file.readlines()
	baktaer = [i.replace("\n", "") for i in baktaer]


TTAN = []
TTAE = []


for i in data:
	try:
		if ttan in i[15]:
			for k in baktana:
				if k in i[11].lower():
					print(True)
					TTAN.append(i)

		# elif ttae in i[15]:
		# 	for k in baktaer:
		# 		if k in i[11].lower():
		# 			TTAE.append(i)
	except TypeError as e:
		pass

for i in data: 
	try:
		for k in baktaer:
			if k in i[11].lower():
				TTAE.append(i)
	except TypeError as e:
		pass

st = run.gen_csv(TTAE)
run.save_csv(st)
