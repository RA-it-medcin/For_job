import nltk
import spacy

import os 
import pandas as pd
import os 
import io
import re 
import sys
import collections as col
import win32com.client
from itertools import chain

import markovify

import numpy as np 


class Work_text(object):
	def __init__(self, *args):
		super(Work_text, self).__init__()

		self.OPEN_FILE = io.open("C:/Users/****/Desktop/Генерация задач 3.0/Формы исходных/задачи.txt",encoding = 'utf-8').readlines()

	def number_task(self,OPEN_FILE):
		self.number_zadaci = []
		for self.index, self.para in enumerate(self.OPEN_FILE):
		  for i2 in range(len(self.para.split(" "))):
		    if "ситуационная" in self.para.split(" ")[i2].lower():
		      self.number_zadaci.append(re.sub("\n","",self.para.split(" ")[i2+3])[1:-1])
		#print(number_zadaci)
		print("Количество задач: ", len(self.number_zadaci))
		return self.number_zadaci

	def index_general_question(self,OPEN_FILE):
		self.index_osn_qeust = [[],[]]
		for self.index,self.para in enumerate(self.OPEN_FILE):
		  self.text = self.para.split("       ")
		  for i in range(len(self.text)):
		    if "основная часть\n" in self.text[0].lower():
		      self.fist_stop = self.index
		    if "вопросы:\n" in self.text[0].lower():
		      self.index_osn_qeust[0].append(self.fist_stop)
		      self.index_osn_qeust[1].append(self.index)
		#print("Индексы начала основной части: ",index_osn_qeust[0])
		#print("Индексы начала вопросов: ",index_osn_qeust[1])
		return self.index_osn_qeust


	def OSN_pats(self,index_osn_qeust,OPEN_FILE):
		self.razdel_po_osn = []
		for i in range(len(self.index_osn_qeust[0])):
			self.a = self.index_osn_qeust[0][i]
			self.b = self.index_osn_qeust[1][i]
			self.zad =[["jjj"]]
			for self.index,self.para in enumerate(self.OPEN_FILE[self.a:self.b]):
				self.perem = self.para.split("       ") 
				if len(self.perem) == 1:
					self.zad[-1] = self.zad[-1]+self.perem
				if len(self.perem) == 2:
					self.zad.append(self.perem)
			self.razdel_po_osn.append(self.zad)

		for i in range(len(self.razdel_po_osn)):
			self.lenn = len(self.razdel_po_osn[i])
			if self.lenn == 1 or self.lenn == 2 or i == 218:
				self.a = self.index_osn_qeust[0][i]
				self.b = self.index_osn_qeust[1][i]
				self.zad = [["jjj"]]
				for self.index,self.para in enumerate(self.OPEN_FILE[self.a:self.b]):
					self.perem = self.para.split("      ") 
					if len(self.perem) == 1:
						self.zad[-1] = self.zad[-1]+self.perem
					if len(self.perem) == 2:
						self.zad.append(self.perem)
				self.razdel_po_osn[i] = self.zad

		return self.razdel_po_osn


	def OSN_pat(self,razdel_po_osn):
		self.text = []
		for i in range(len(self.razdel_po_osn)):
			self.bb = "".join(self.razdel_po_osn[i][1])
			self.text.append(str(self.bb))

		self.text2 = self.text.copy()
		for i in range(len(self.text2)):
			self.a = " ".join(self.text[i].split("   ")[0].split("\n"))
			self.text2[i] = str(self.a)
		return self.text2

	def text_fun(self,text2):
		self.text2_text = []
		self.t = 0
		for i in range(len(self.text2)):
			self.split_text2 = self.text2[i].split(".")
			if len(self.split_text2[0]) == 9 or len(self.split_text2[0]) == 10 or len(self.split_text2[0]) == 11:
				self.split_text2[0] = self.split_text2[0]+"."+self.split_text2[1]
				del self.split_text2[1]
			if len(self.split_text2[-1]) == 1:
				self.split_text2[-1] = self.split_text2[-2]+self.split_text2[-1]
				del self.split_text2[-2]
			self.t += len(self.split_text2)
			self.text2_text.append(self.split_text2)
		self.sr_kof = 4 #int(self.t/len(self.text2_text)) #подмена
		print("Среднее количество предложений:",self.sr_kof)
		self.not_sort = []
		self.pred = [[]*o for o in range(self.sr_kof)]
		self.index_pred = [[]*o for o in range(self.sr_kof)]
		for i in range(len(self.text2_text)):
			#print(text2_text[i],len(text2_text[i]))
			if len(self.text2_text[i])<=self.sr_kof:
				for i2 in range(len(self.text2_text[i])):
					self.pred[i2].append(self.text2_text[i][i2])
					self.index_pred[i2].append(i)
			elif len(self.text2_text)>self.sr_kof:
				for i3 in range(len(self.text2_text[i][:self.sr_kof])):
					self.pred[i3].append(self.text2_text[i][i3])
					self.index_pred[i3].append(i)
				for i4 in range(len(self.text2_text[i][self.sr_kof+1:])):
					self.not_sort.append(self.text2_text[i][i4])

		self.kol_vo_simvol = []

		self.new_model_text = [[]*o for o in range(self.sr_kof)]
		for i in range(len(self.pred)):
			self.t = 0
			for i2 in range(len(self.pred[i])):
				self.t += len(self.pred[i][i2]) 
				self.b = markovify.Text(self.pred[i][i2],well_formed=False)
				self.new_model_text[i].append(self.b)
			self.kol_vo_simvol.append(int(self.t/len(self.pred[i])))
		print("Количество символов:",self.kol_vo_simvol)
		print("Размеры значений",[len(self.pred[o]) for o in range(len(self.pred))])

		self.not_sort_Text = []
		t = 0
		for i in range(len(self.not_sort)):
			self.b = markovify.Text(self.not_sort[i],well_formed=False)
			self.not_sort_Text.append(self.b)
			self.t+=len(self.not_sort[i])
		self.sim_not_sort = int(self.t/len(self.not_sort))
		print("Количество символов в несортированном:",self.sim_not_sort)

		return self.new_model_text, self.not_sort_Text,self.kol_vo_simvol,self.sim_not_sort


	def labor(self,razdel_po_osn,):
		self.OAK = []
		self.OAK_index = []
		self.BH = []
		self.BH_index = []
		#ECHO = []
		for i in range(len(self.razdel_po_osn)):
			for i2 in range(2,len(self.razdel_po_osn[i])):
				self.gg = "".join(self.razdel_po_osn[i][i2])
				#print(gg) #тут вы можете поэксперементировать 
						#(уберите # перед print(gg), и получите листы с раличными показателями)
						#логика проста создайте переменную по типу OAK\BH (аналагичная строчка с другими буквами)
						#например Эхо-КГ:
						#на ряду с командами if создайте найденную закономерность, в случае с Эхо-КГ: по типу if "ЭХО-КГ:".lower() in gg2.lower()
						#ECHO.append(gg)
				self.gg2 = self.gg.split(" ")
				if  "Общий" in self.gg2 and "анализ" in self.gg2 and "крови:" in self.gg2 or "Биохимический" not in self.gg2 and "анализ" in self.gg2 and "крови:" in self.gg2 or "В анализах:" in self.gg2:
					self.OAK.append(self.gg)
					self.OAK_index.append(i)
				if "Биохимический" in self.gg2 and "анализ"  in self.gg2 and "крови:"  in self.gg2:
					self.BH.append(self.gg)
					self.BH_index.append(i)

		self.name_BH = []
		self.znac_BH = []
		for i in range(len(self.BH)):
			self.BH[i] = self.BH[i].replace("\n"," ")
			self.BH_split = self.BH[i].split(", ")
			if len(self.BH_split) == 1:
				self.BH_split = self.BH_split[0].split("; ")
			for i2 in range(len(self.BH_split)):
				self.peremen = self.BH_split[i2].split("-")
				if len(self.peremen)==1:
					self.peremen = self.peremen[0].split("–")
				#print(peremen,len(peremen),number_zadaci[BH_index[i]])
				if len(self.peremen)>2:
					print(print(self.peremen,len(self.peremen),self.number_zadaci[self.BH_index[i]]))
					sys.exit()
				self.name_BH.append(self.peremen[0])
				self.znac_BH.append(self.peremen[1])
		print("Имена показателей, значение:",len(self.name_BH),len(self.znac_BH))

		self.name_OAK = []
		self.znac_OAK = []
		for i in range(len(self.OAK)):
			self.OAK[i] = self.OAK[i].replace("\n"," ")
			self.OAK_split = self.OAK[i].split(", ")
			if len(self.OAK_split) == 1:
				self.OAK_split = self.OAK_split[0].split("; ")
			for i2 in range(len(self.OAK_split)):
				self.peremen = self.OAK_split[i2].split("-")
				if len(self.peremen)==1:
					self.peremen = self.peremen[0].split("–")
				#print(peremen,len(peremen),number_zadaci[OAK_index[i]])
				if len(self.peremen)>2:
					print(self.peremen,len(self.peremen),self.number_zadaci[self.OAK_index[i]])
					sys.exit()
				self.name_OAK.append(self.peremen[0])
				self.znac_OAK.append(self.peremen[1])
		print("Имена показателей, значение:",len(self.name_OAK),len(self.znac_OAK))

		return self.OAK,self.name_OAK,self.znac_OAK, self.BH,self.name_BH,self.znac_BH

	def Predlozenia(self,new_model_text,not_sort_Text,kol_vo_simvol,sim_not_sort,OAK_1,BH_1):
		print("--------------------------------------")
		print("Текст задачи:","\n")
		self.struc = ""
		for i in range(len(new_model_text)):
			self.model = markovify.combine(new_model_text[i])
			self.struc += self.model.make_sentence(tries=kol_vo_simvol[i])+". "
		print("Основное предложение: --",self.struc)
		self.model_not_sort = (markovify.combine(not_sort_Text)).make_sentence(tries=sim_not_sort)
		print("Не сортированое предложение: -- ",self.model_not_sort)

		def labor_gen(OAK_,hh):
			t = 0
			OAK_Text = []
			for i in range(len(OAK_)):
				b = markovify.Text(OAK_[i],well_formed=False)
				OAK_Text.append(b)
				t+=len(OAK_[i])
			kol_vo_simvol = int(t/len(OAK_Text))
			#print("Количество символов в ОАК:",kol_vo_simvol)

			model = markovify.combine(OAK_Text)
			model =  model.make_sentence(tries=kol_vo_simvol)+". ".replace("; ",",")
			if hh == 0:
				print("ОАК: --",model)
			elif hh == 1:
				print("БХ: -- ", model)

			return model
		labor_gen_OAk = labor_gen(OAK_1,hh=0)
		labor_gen_BH = labor_gen(BH_1,hh =1)



		return self.struc, self.model_not_sort


	def srodstvo_zad(self,struc,text2,number_zadaci):
		self.list_struc = struc.split(" ")
		self.kol_sovp = []
		for o in range(len(text2)):
			self.t = 0
			for i in range(len(self.list_struc)):
				self.a = text2[o].count(self.list_struc[i])
				if self.a != 0:
					self.t+=self.a
				else:
					pass
			self.yyy = self.t/len(text2[o])
			self.kol_sovp.append(float("%.2f" %self.yyy))

		self.dict_col = dict(zip(number_zadaci,self.kol_sovp))
		self.sorted_tuples = sorted(self.dict_col.items(), key=lambda item: item[1])
		self.sorted_dict = {k: v for k, v in self.sorted_tuples}
		self.task_name = list(self.sorted_dict.keys())
		self.task_name.reverse()
		self.znac_task = list(self.sorted_dict.values())
		self.znac_task.reverse()
		print("Порядковые значения:\n",self.task_name[:5],"\n",self.znac_task[:5])

class Work_answer(object):
	def __init__(self, *args):
		super(Work_answer, self).__init__()

		self.OPEN_FILE_A = io.open("C:/Users/****/Desktop/Генерация задач 3.0/Формы исходных/ответы.txt",encoding = 'utf-8').readlines()

	def number_task_answer(self,OPEN_FILE_A):
		self.number_zadaci = []
		for self.index, self.para in enumerate(self.OPEN_FILE_A):
			for i2 in range(len(self.para.split(" "))):
				if "ситуационная" in self.para.split(" ")[i2].lower():
					self.hh = re.sub("\n","",self.para.split(" ")[i2+3])[1:-1]
					self.number_zadaci.append(self.hh)
		#print(number_zadaci)
		print("Количество задач: ", len(self.number_zadaci))
		return self.number_zadaci

	def answer_1(self,OPEN_FILE_A):
		self.diagnoz = []
		self.one = []
		self.two = []
		for self.index, self.para in enumerate(self.OPEN_FILE_A):
			if "     1." in self.para:
				self.one_tup = self.index
			if "    2. " in self.para:
				self.one.append(self.one_tup)
				self.two.append(self.index)

		print("Количество воспросов от 1 до 2:",len(self.one),len(self.two))
		for i in range(len(self.one)):
			self.a = re.sub("[xc|\n]","","\n".join(self.OPEN_FILE_A[self.one[i]:self.two[i]-1]))
			self.a = self.a.split("                       ")
			self.diagnoz.append(self.a[0])
			#print(diagnoz[i],"\n---------------")
		print("Количство предположительных диагнозов:",len(self.diagnoz))
		return self.diagnoz

	def Qestion(self,OPEN_FILE_1,number_zadaci_1):
		self.index_osn_qeust = []
		for self.index,self.para in enumerate(OPEN_FILE_1):
			self.text = self.para.split("       ")
			for i in range(len(self.text)):
				if "вопросы:\n" in self.text[0].lower():
					if "1. " in OPEN_FILE_1[self.index+2]:
						self.index_osn_qeust.append(OPEN_FILE_1[self.index+2])
						#print(OPEN_FILE_1[index+2])
					else:
						self.index_osn_qeust.append(OPEN_FILE_1[self.index+1])
						#print(OPEN_FILE_1[index+1])
		print("Количество 1 вопросов:",len(self.index_osn_qeust))

		self.new_quest = []
		self.new_zadaci = []
		for i in range(len(self.index_osn_qeust)):
			if "Предположите" in self.index_osn_qeust[i] or "Сформулируйте" in self.index_osn_qeust[i] or "Наиболее" in self.index_osn_qeust[i] or "Назовите" in self.index_osn_qeust[i] or "Поставьте" in self.index_osn_qeust[i]:
				self.new_zadaci.append(number_zadaci_1[i])
				self.new_quest.append(self.index_osn_qeust[i])
			else:
				pass
		print("Количество сохранившихся задач, по известному диагнозу:",len(self.new_quest),len(self.new_zadaci))

		return self.new_quest,self.new_zadaci

	def Vozrat_zadac(self,number_zadaci,diagnoz,Qestion_diagnoz):
		self.number_zadaci_new = self.number_zadaci.copy()
		self.diagnoz_new = self.diagnoz.copy()
		self.t  = 0
		for i in range(len(self.number_zadaci)):
			self.a = self.number_zadaci[i]
			if self.a not in Qestion_diagnoz[1]:
				del self.number_zadaci_new[i-self.t]
				del self.diagnoz_new[i-self.t]
				self.t +=1
		print("Количество переработаных диагнозов:",len(self.number_zadaci_new),len(self.diagnoz_new))

		return self.number_zadaci_new,self.diagnoz_new

	def work_znac_OAK(self,znac_OAK_):
		self.znac_float = []
		for i in range(len(znac_OAK_)):
			self.a = znac_OAK_[i].split("×")
			if len(self.a)>1:
				znac_OAK_[i] = self.a[0]
			if znac_OAK_[i] == " без особенностей" or znac_OAK_[i] == " норма":
				self.znac_ = "норма"
			else:
				self.znac_ = re.sub("[%|мм/ч|г/л|мм/час.|мм/ч.|)|ммоль/л|мкмоль/л.|фл|пг|мкМЕ/мл|пкмоль/л.|fl|д|U/L.|везрения|ЕД/л]| ","",znac_OAK_[i])
				#print(znac_OAK_[i],znac_)
				self.znac_ = float(re.sub(",",".",self.znac_))
			self.znac_float.append(self.znac_)
			#print(znac_OAK_[i],znac_)

		return self.znac_float

	def Predlozeni_answer(self,fun_text): 
		self.text_model = []
		self.lean_a_list = []
		self.t = 0
		for i in range(len(fun_text)):
			self.a = fun_text[i].split("  1.")[1]
			self.a = self.a.split(".")
			self.len_a = len(self.a)
			self.lean_a_list.append(self.len_a)
			if len(self.a[-1])<1:
				del self.a[-1]
			for i2 in range(len(self.a)):
				self.t+=len(self.a[i2])
				self.b = markovify.Text(self.a[i2], well_formed = False)
				self.text_model.append(self.b)

		self.T = int(self.t/len(self.lean_a_list))
		

		self.model = markovify.combine(self.text_model)
		self.model = self.model.make_sentence(tries = self.T)
		print("Диагноз: -- ",self.model,"\n")

		print("Количество символов:",self.T)
		print("Среднее количество предложений:",int(np.mean(self.lean_a_list)),"Макс:",max(self.lean_a_list))
		return self.model



class Work_index_answer_task(object):
	def __init__(self, *args):
		super(Work_index_answer_task, self).__init__()
		
		self.OPEN_FILE__T = io.open("C:/Users/Tama/Desktop/Генерация задач 3.0/Формы исходных/задачи.txt",encoding = 'utf-8').readlines()
		self.OPEN_FILE__A = io.open("C:/Users/Tama/Desktop/Генерация задач 3.0/Формы исходных/ответы.txt",encoding = 'utf-8').readlines()

	def number_task_All(self,File,name):
		self.number_zadaci = []
		for self.index, self.para in enumerate(File):
			for i2 in range(len(self.para.split(" "))):
				if "ситуационная" in self.para.split(" ")[i2].lower():
					self.hh = re.sub("\n","",self.para.split(" ")[i2+3])[1:-1]
					self.number_zadaci.append(self.hh)
		#print(number_zadaci)

		print("Количество задач "+name+": ", len(self.number_zadaci))
		return self.number_zadaci

	def Analiz_task_answer(self,a,b):
		self.sort_task = []
		for i in range(len(b)):
			if b[i] in a:
				self.sort_task.append(b[i])
			else:
				pass
		print("Количество совпадающих задач:", len(self.sort_task))
		return self.sort_task

	def viclinenie_diagnoz(self,TA,D,RT):
		self.r_diagnoz = []
		self.r_task_di = []
		for i in range(len(RT)):
			if RT[i] not in TA:
				pass
			else:
				self.perem_index = TA.index(RT[i])
				self.r_diagnoz.append(D[self.perem_index])
				self.r_task_di.append(RT[i])
		print("Количество возвращеных задач и диагнозов: ", len(self.r_diagnoz))
		return self.r_task_di,self.r_diagnoz



class work_soot_tast_answer(object):
	"""docstring for work_soot_tast_answer"""
	def __init__(self, *args):
		super(work_soot_tast_answer, self).__init__()

	def Save_to_csv():
		IN = os.listdir(os.getcwd())
		if "ICD-10.csv" in IN:
			return pd.read_csv("ICD-10.csv", delimiter ="&")
		elif "ICD-10.csv" not in IN:
			ICD = pd.read_excel("ICD-10.xlsx",sheet_name = 0)
			ICD.to_csv("ICD-10.csv",sep = "&", encoding = "utf-8",)
			ICD = pd.read_csv("ICD-10.csv", delimiter ="&")
			return ICD
	ICD = Save_to_csv()

	def ICD_soot(self,DF_ICD,N_T,A):
		print("Имена столбцов МКБ-10:",list(DF_ICD.columns))
		for i in range(len(A)):
			A[i] = A[i].split(". ")[1:]
			A[i] = ". ".join(A[i]).lower()
			A[i] = A[i].split(" ")
			t = 0
			for i2 in range(len(A[i])):
				if len(A[i][i2-t]) == 0:
					del A[i][i2-t]
					t+=1
				else:
					pass
			A[i] = " ".join(A[i])
			A[i] = A[i].split(".")[0] 
			#print(A[i],"\n----------")
		A_copy = A.copy()
		codirovka_icd = [[]*u for u in range(len(A_copy))]

		

		yt1 = DF_ICD[list(DF_ICD.columns)[1]].to_list()
		yt1 = [yt1[i] for i in range(len(yt1)) if yt1[i]<15]

		yt = DF_ICD[list(DF_ICD.columns)[-1]].to_list()
		yt = [str(yt[i]).lower() for i in range(len(yt1))]

		for i in range(len(A_copy)):
			Sort = A_copy[i].lower().split(" ")
			if "основной" in Sort and "диагноз" in Sort or "основной" in Sort and "диагноз:" in Sort:
				if "основной" in Sort:
					del Sort[Sort.index("основной")]
				if "диагноз" in Sort:
					del Sort[Sort.index("диагноз")]
				if "диагноз:" in Sort:
					del Sort[Sort.index("диагноз:")]
			A_copy[i] = " ".join(Sort)
			text_A_copy_split = A_copy[i].lower()
			#print(text_A_copy_split)
			tokens = nltk.word_tokenize(text_A_copy_split)
			bigram = list(nltk.ngrams(tokens, 2))
			for i2 in range(len(bigram)):
				#print('Популярные биграммы: ', " ".join(bigram[i2]) )
				Bigram_str = " ".join(bigram[i2])
				for i3 in range(len(yt)):
					if Bigram_str.lower() in yt[i3]:
						codirovka_icd[i].append(yt1[i3])
			form = col.Counter(codirovka_icd[i])
			if len(form) == 0:
				text_A_copy_split_1 = text_A_copy_split.split(" ")
				#print(text_A_copy_split_1)
				for i4 in range(len(text_A_copy_split_1)):
					for i5 in range(len(yt)):
						if text_A_copy_split_1[i4] in yt[i5]:
							codirovka_icd[i].append(yt1[i5])
			else:
				pass
			#print(col.Counter(codirovka_icd[i]))
			codirovka_icd[i] = list(col.Counter(codirovka_icd[i]).keys())

		matrix_data = np.zeros((len(N_T), len(list(col.Counter(yt1).keys()))))

		for i in range(len(codirovka_icd)):
			for i2 in range(len(codirovka_icd[i])):
				b = codirovka_icd[i][i2]
				matrix_data[i][b-1] = b


		DF_ICD = pd.DataFrame({"Номер задачи":N_T,"Диагноз": A_copy,"Найденные Классы МКБ-10":codirovka_icd})
		DF_ICD_1 = pd.DataFrame(matrix_data, columns = [str(i) for i in range(1,len(list(col.Counter(yt1).keys()))+1)])
		DF_ICD = pd.concat([DF_ICD,DF_ICD_1],1)
		DF_ICD.to_excel("Кодировка.xlsx")
		return DF_ICD
		


class Generate_new_task(object):
	"""docstring for Generate_new_task"""
	def __init__(self, *args):
		super(Generate_new_task, self).__init__()

	def work_DF(self,DF,text,NTZ):
		print("Инмена листа:",list(DF.columns))
		Y = 9
		Df = DF.loc[DF[str(Y)] == Y]
		Df_list_nt = Df["Номер задачи"].to_list()
		Df_list_di = Df["Диагноз"].to_list()
		new__text2 = []
		answer__text2 = []
		for i in range(len(Df_list_nt)):
			index = NTZ.index(Df_list_nt[i])
			new__text2.append(text[index])
			answer__text2.append(Df_list_di[i])

		return new__text2,answer__text2

	def New_predlogenia(self,a):
		kof = 0
		for i in range(len(a)):
			kof +=len(a[i])
			a[i] = markovify.Text(a[i],well_formed = False)

		kof = int(kof/len(a))
		model = markovify.combine(a)
		model = model.make_sentence(tries = kof)
		print("Диагноз:",model)




__name__ = "__main1__"
if __name__ == "__main1__":
	print("_____Запуск Class3__part 1__")
	Class3 = Work_index_answer_task()  #Запуск класа 3 отвечащий за Сопоставление диагнозов
	Task_T = Class3.number_task_All(Class3.OPEN_FILE__T,"в задачах") #Загрузка и выгрузка номеров задач
	Task_A = Class3.number_task_All(Class3.OPEN_FILE__A,"в ответах") #Загр и выгр номеров задач в ответах
	Sootvestvie_T_A = Class3.Analiz_task_answer(Task_T,Task_A) # Проверка сооствествия задач в задачах и задач в ответах
	diagnozis = Work_answer().answer_1(Class3.OPEN_FILE__A) #Выгрузка 1 вопроса в основном отвечающих за диагноз
	vozrat_zadach_di,vozrat_diagnozis = Class3.viclinenie_diagnoz(Task_A,diagnozis,Sootvestvie_T_A) #Сортировка по наличию номеров задач

	print("_____Запуск Class1__")
	Class1 = Work_answer() #Запуск класа 1 отвечающего за работу с ответами
	N_Z_A = Class1.number_task_answer(Class1.OPEN_FILE_A) #номера задач
	A_1 = Class1.answer_1(Class1.OPEN_FILE_A) #Выгрузка 1 вопроса в основном отвечающих за диагноз
	Qestion_diagnoz = Class1.Qestion(Class3.OPEN_FILE__T,Task_T)# Фильтр по вопросам оставляющий 1 вопрос являющийся ответом на задачу
	Vozrat_zad = Class1.Vozrat_zadac(N_Z_A,A_1,Qestion_diagnoz) #Возвращаем номера задач с ответом диагноза

	print("_____Запуск Class3__part 2__")
	vozrat_zadach_di_1,vozrat_diagnozis_1 = Class3.viclinenie_diagnoz(vozrat_zadach_di,vozrat_diagnozis,Vozrat_zad[0]) #Проверка на совместимость для точности.

	print("_____Запуск Class4__")
	Class4 = work_soot_tast_answer() #нахождеие общих задач и соответствие их коду МКБ-10
	Kod_icd_df = Class4.ICD_soot(Class4.ICD,vozrat_zadach_di_1,vozrat_diagnozis_1) #создание датасета по диагнозу и соответствующему ему класса

	print("_____Запуст Class0___part 1__")
	Class0 = Work_text() #Загрузка фунций класаа0 отвечающего за работу с текстом задач
	N_Z_T = Class0.number_task(Class0.OPEN_FILE) #возрат номеров задач
	I_G_Q = Class0.index_general_question(Class0.OPEN_FILE) #индекс основной части содержащей Анамнез, лабораторную часть, Инструментальню
	OSN_pats_ = Class0.OSN_pats(I_G_Q,Class0.OPEN_FILE) #возращает razdel_po_osnovam (I_G_Q разделение)
	OSN_pat_ = Class0.OSN_pat(OSN_pats_) #возвращает список жалоб и грубо говоря Анамнез
	Osnova = Class0.text_fun(OSN_pat_) #возвращает сортированный список (OSN_pats_) на сортированые, не сортированые значения, и среднее количество символов в них
	OAK_ , name_OAK_, znac_OAK_,BH_,name_BH_,znac_BH_ = Class0.labor(OSN_pats_) #возвращает имена и значения показателей по ОАК И БХ и их исчесления

	print("_____Запуск Class5__")
	Class5 = Generate_new_task() #Отвечает за генерацию соответсвующих задач
	work_DF_text,work_DF_answer = Class5.work_DF(Kod_icd_df,OSN_pat_,N_Z_T) #посылается текст в зависимости от класса заболевания

	print("_____Запуск Class0___part 2__")
	Osnova1 = Class0.text_fun(work_DF_text)

	#Вывод текста на основе формы Class5:
	Predlozenia_ = Class0.Predlozenia(Osnova1[0],Osnova1[1],Osnova1[2],Osnova1[3],OAK_,BH_)
	Predlozeni_answer_ = Class5.New_predlogenia(work_DF_answer)

if __name__ == "__main__":
	#Наследуемые из Class0
	print("_____Запуст Class0__")
	Class0 = Work_text()
	N_Z_T = Class0.number_task(Class0.OPEN_FILE)
	I_G_Q = Class0.index_general_question(Class0.OPEN_FILE)
	OSN_pats_ = Class0.OSN_pats(I_G_Q,Class0.OPEN_FILE)
	OSN_pat_ = Class0.OSN_pat(OSN_pats_)
	Osnova = Class0.text_fun(OSN_pat_)
	OAK_ , name_OAK_, znac_OAK_,BH_,name_BH_,znac_BH_ = Class0.labor(OSN_pats_)

	#Наследуемые из Class1
	print("_____Запуст Class1__")
	Class1 = Work_answer()
	N_Z_A = Class1.number_task_answer(Class1.OPEN_FILE_A)
	A_1 = Class1.answer_1(Class1.OPEN_FILE_A)
	Qestion_diagnoz = Class1.Qestion(Class0.OPEN_FILE,N_Z_T)
	Vozrat_zad = Class1.Vozrat_zadac(N_Z_A,A_1,Qestion_diagnoz)

	#Формировние предложения
	Predlozenia_ = Class0.Predlozenia(Osnova[0],Osnova[1],Osnova[2],Osnova[3],OAK_,BH_)
	Predlozeni_answer_ = Class1.Predlozeni_answer(Vozrat_zad[1])

	#Проверка на сродство генерируемого текста к задаче
	print("\n\n")
	srodstvo_zad_ = Class0.srodstvo_zad(Predlozenia_[0],OSN_pat_,N_Z_T)

	#for DataFrame:
	znac_float_list_OAK = Class1.work_znac_OAK(znac_OAK_)
	znac_float_list_BH = Class1.work_znac_OAK(znac_BH_)
