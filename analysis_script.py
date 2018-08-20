# Analyzing the patient registries data sheets
# for data extraction and modification
# (cc) 2018 Ali Rassolie
# Klinisk Mikrobiologi
# Karolinska Universitetssjukhus Huddinge, Stockholm, Sweden

print("[GLOBAL] Importing")
import pandas as pd
from collections import *
print("[GLOBAL] Finished import")

class KlinMikroTools:
	def __init__(self):
		print("[GLOBAL] Configuration")
		with open("config.yaml", "r") as file:
			config = file.readlines()
			config = [i.replace("\n", "") for i in config]
			self.config = {i.split(": ")[0]:i.split(": ")[1] for i in config}
			print(config)

	def load_excel(self, xlsFile: str = None, config: dict = None):
	# Will be used to return an opened excel file in order 
	# to be used in conjunction with the load_data_excel method. 
		print("[load_excel] Running")

	# Bunch of if-statements so as to make sure that we dont 
	# get any conflicts regarding the naming of the files. 
		if xlsFile: file = xlsFile
		elif config: file = config["FILE_NAME"]
		else: file = self.config["FILE_NAME"]

	# we read the excel file by using some pandas methods
		print("[load_excel] Reading excel")
		xlsFile = pd.ExcelFile(file)
		print("[load_excel] Finished reading excel")
		
		sheetnames = xlsFile.sheet_names

	# we return a pandas object and the sheetnames (also
	# a pandas object?)

		return xlsFile, sheetnames

	def load_data_excel(self, 
						xlsFile, 
						sheetName: str = None, 
						nativeList: bool = False) -> (list, list):
	# load_data_excel() 
	# xlsFile:    is the pandas opened ExcelFile
	# sheetName:  is the name of the specific sheet that 
	# 			  the one likes to be read
	# nativeList: a bool used to return a native python
	# 			  list, instead of returning a pandas.DataFrame

	# We use the parse method to return the contents of the spec
	# sheet in the excelfile
		print("[load_data_excel] Running")
		data = xlsFile.parse(sheetName)
		vals = data.values
		keys = data.columns
		if nativeList:
			newvals = []
			for i in vals:
				newvals.append(list(i))
			vals = newvals

		print("[load_data_excel] Returning")
		return keys, vals

	def load_data_csv(self, csvfile: str) -> list:
		
		print("[load_data_csv] Running")
		if csvfile: path = csvfile
		else: path = self.config["CSV_FILE"]
		with open(path, "r") as file:
			data = file.readlines()
			data = [i.replace("\n", "") for i in data]
			ed   = [i.split(",") for i in data]
		return ed

	def gen_csv(self, 
				dataset: list, 
				keyword: str = None) -> str:
	# Input is a native python 2D list, which will generate
	# a csv str that can be saved. This csv string will be 
	# returned. Can be easily be parsed into save_csv in order
	# to output a csv file. 
		print("[gen_csv] Running Method")
		if keyword: saveto = f"{keyword}_{self.config['OUTPUT_CSV']}"
		else: saveto = self.config["OUTPUT_CSV"]
		
		str_to_write = ""
		for ls in dataset: 
			for i in ls:
				i = str(i)
				
				try:
					str_to_write = str_to_write + "," + i
				except Exception as e:
				
					raise e
			str_to_write += "\n"
			
		# print(str_to_write)
		print("[gen_csv] Finished")
		return str_to_write

	def save_csv(self, 
		str_to_write: str, 
		keyword:	  str = "Hello"):

		if keyword: saveto = f"{keyword}_{self.config['OUTPUT_CSV']}"
		else: saveto = self.config["OUTPUT_CSV"]
		with open(saveto, "w") as file:
			file.write(str_to_write)

	def sort_by(self, 
				config, 
				keyword = "Födelsedatum"):

		dataset = load_data_csv(config = config)
		dataset[0].append("Index\n")
		
		# BirthDayIndex
		BDI = dataset[0].index(keyword)
		boo  = False
		temp = 0

		for i, ls in enumerate(dataset[1:]):
			i += 1
			if temp == ls[BDI]:
				boo = True
				dataset[i].append("1\n")

			elif temp != ls[BDI]:
				boo = False
				temp = ls[BDI]
				dataset[i].append("0\n")

			else:
				print("[sort_by] Error") 

	def produce_lines(self):
	# produce_lines
	# Specifically made so as to evaluate the times in 
	# the excel file
		data  = self.load_data_csv()
		# cols  = data[0]
		lines = data[1:]
		d_frys  = [i[3:] for i in lines]
		d_times = [i[:3] for i in lines]

		return d_times, d_frys

	def fix_AP(self, 
			   data: list, 
			   yearIndex: int, 
			   apIndex: int) -> list:
	# fix_AP
	# a method where we will be incorporating the "{year}AP" 
	# prefix. Used such that it will be easier to search through
	# the datalists
		findata = []
		for i in data:
			if   "5" in str(i[yearIndex]): t = f"15AP{i[apIndex]}"
			elif "6" in str(i[yearIndex]): t = f"16AP{i[apIndex]}"
			elif "7" in str(i[yearIndex]): t = f"17AP{i[apIndex]}"
			elif "8" in str(i[yearIndex]): t = f"18AP{i[apIndex]}"
			
			else: t = f"Err{i[apIndex]}"
			findata.append([t, i[8]])

		return findata

	def sort_times(self, 
				   times: list, 
				   frys: list) -> list:
		# times, frys = self.produce_lines()
		frys2 = []
		print(times[:2],"\n\n" , frys[:3])
		for fr in frys: 
			frys2.append(fr)
			for i in times:
				try:
					if i[0] in fr[0]:
						frys2[-1].append(i[-1])
					
				except TypeError as e:
					# print(i[0], fr[0])
					pass
		return frys2

	def sort_frys(self, 
				  xlsFile, 
				  sheetnames: list, 
				  keyword: list =[""]) -> list:
	# sort_frys()
	# A method used to sort the fryslistor
		print("[sort_frys] Running method", sheetnames[0])
		frys = []
		for i in sheetnames:
			keys, vals = run.load_data_excel(xlsFile, i, nativeList=True)
			for k in vals:
				try:
					k[3] = k[3].lower()
					frys.append(k)

				# The excelfiles are not always clean
				# hence this precaution, such that we may skip the 
				# empty ones.
				except AttributeError as e:
					frys.append(k)
		# print(frys)
		sortList = []
		for i in frys:
			for key in keyword:
				try: 
					if key in i[3]:
						# print(i)
						sortList.append(i)
				except TypeError as e:
					pass
		return sortList


	def do_repl_job(self, 
					data:      list,
					character: str, 
					index:     int,
					start:     int = None,
					stop:      int = None,
					step:      int = None) -> list:
	# do_repl_job
	# a method that should be present natively
	# but I couldnt be bothered looking for it. 
	# A simple solution.
	# data:      is a 1D list of strings, not 2D. 
	# character: is the character that we will be
    #			 looking for.

	# we create a slice object, that then can be used
	# i conjunction with the native python list. 
	# This way, we can more easily parameterize the 
	# slicing. 
		sl      = slice(start,stop,step)
		outlist = []
		for i in data:
			if character in i[index]:
				outlist.append(i[sl].lower())
				
			else:
				outlist.append(i.lower())
				
		return outlist
		
	def search_for_bacteria(self, 
							vals: 	   list, 
							bactIndex: int = 3, 
							posIndex:  int = 6) -> dict:
	# search_for_bacteria
	# This method is used in order to search, clean and count
	# the collected bacteria. 
	# vals: one parses in the vals from the excel file, which 
	# 		we assume to contain a column for the bacteria

		searchfor = ["actinobaculum","actinomy", "actinotignum","anaerococcus",
					"bacteroid","bifi","clostr",
					"dialister","eggerthella","finegoldia",
					"fusobac","gardner","lactobac",
					"lactoco","parvim","peptonip",
					"prevote", "solobact", "veillon"]

	# the indices here are taken from the excelfile, in order to be done
		bacteria  = [i[3] for i in vals]
		pos       = [i[6] for i in vals]
		bacteria  = self.do_repl_job(bacteria, " ", 0, 1,-1)

	# countBact dict, where each search-term is associated
	# with a list of pos, neg or undef  count-values, init
	# at 0.
		countBact = {i: [0, 0, 0] for i in searchfor}
		keys = list(countBact.keys())

		for i in keys:
			for ind, k in enumerate(bacteria):
			# These if statements are evaluating whether
			# the bacteria in question was registered pos, neg
			# or undef (1,0, or 2), 
				if i in k and pos[ind] == 1:
					countBact[i][0] += 1

				elif i in k and pos[ind] == 0:
					countBact[i][1] += 1

				elif i in k and pos[ind] == 2:
					countBact[i][-1] += 1

	# Will print the countBact dictionary in order to 
	# easily visualize the values that we get.
		for i in countBact:
			print(i, countBact[i])

		return countBact



	def extract_frys(self, clean: bool = True) -> str:
	# exctract_frys
	# designed to evaluate one or more fryslistor
	# in order to extract the searched for keywords.
	# Note that in this iteration, we have preset
	# indices for extracting the data. 

		frysfiler = ["Fryslista_AP_2015_VO.xlsx",
					"Fryslista_AP_2016_VO.xlsx",
					"Fryslista_AP_2017_VO.xlsx",
					"Fryslista_AP_2018_VO.xlsx"]

		keywords = ["actinobaculum","actinomy", "actinotignum","anaerococcus",
						"bacteroid","bifi","clostr",
						"dialister","eggerthella","finegoldia",
						"fusobac","gardner","lactobac",
						"lactoco","parvim","peptonip",
						"prevote","solobact","veillon"]

		frysList = []
		# iterate through the frysfiler
		for fil in frysfiler:
		# We load the excelfile
			xlsFile, sheetnames = self.load_excel(fil)
		# We run sort_frys, by inputting the excelfile, 
		# the sheetnames and the keywords
		# this will return an array
			k = self.sort_frys(xlsFile, sheetnames, keywords)

			for i in k: frysList.append(i)

		print(frysList)
		if clean:
			bacteria = [i[3] for i in frysList]
			bacteria = self.do_repl_job(bacteria, " ", 0, 1, None)
			print(bacteria)

		frysList2 = []
		for i, b in zip(frysList, bacteria):
			i[3] = b
			frysList2.append(i)

		str_to_write = self.gen_csv(frysList2)

		self.save_csv(str_to_write)
