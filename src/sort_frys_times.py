from analysis_script import KlinMikroTools

times = [i[:2] for i in data]
frys  = [i[2:] for i in data]
frys2  = run.sort_times(times, frys)

st   = run.gen_csv(frys)
run.save_csv(st)

cleanedAP    = run.fix_AP(data, 0, 1)
str_to_write = run.gen(cleanedAP)
run.save_csv(str_to_write)

first  = [i[:3] for i in data]
second = [i[3:] for i in data]

newData = []
for i in second:
	newData.append(i)
	for k in first:
		try:
			if i[1].upper() == k[1].upper():
				newData[-1].append(k[-1])
		except AttributeError as e:
			pass
