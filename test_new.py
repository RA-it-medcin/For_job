from import_data import *
print(len(a))

def Analizi(x,name,analiz_min0,analiz_max0):
	

	def Read_Zadac(ZADACA1,name):
		return_big_level = []
		for nomer_zadaci in range(len(ZADACA1)):
			#загрузка значений по анализам
			MAX_znac = ZADACA1[nomer_zadaci]["Max"].tolist()
			vvod_znac = ZADACA1[nomer_zadaci]["vvod"].tolist()
			MIN_znac = ZADACA1[nomer_zadaci]["Min"].tolist()
			level1 = []
			for i in range(len(MAX_znac)):
				a1 = MAX_znac[i]
				c = vvod_znac[i]
				b = MIN_znac[i]
				if b<=c<=a1:
					level1.append("Norm")
				if b>c:
					level1.append("Low")
				if a1<c:
					level1.append("High")
			return_big_level.append(level1)
		for i in range(len(ZADACA1)):
			df = pd.DataFrame({"level": return_big_level[i]})
			ZADACA1_save = pd.concat([ZADACA1[i], df],axis = 1)
			#сохранение анализов в один лист
			ZADACA1_save.to_excel(pyt_save_zadac + "/" + name[i], sheet_name = "0" )

		return return_big_level
	return_level = Read_Zadac(x,name)

	def Data_Frame_at_level(return_level,analiz_min0,analiz_max0,name):
		big_analiz_level_max = []
		big_analiz_level_min = []
		for i in range(len(return_level)):
			level = list(return_level[i]) 
			name_keys = list(analiz_min0.keys())
			#print(name_keys)
			analiz_level_max = []
			analiz_level_min = []
			for i2 in range(len(level)):
				g = level[i2]
				g2 = name_keys[i2]
				if g =="Norm":
					analiz_level_min.append([0] * len(analiz_min0[g2].tolist()))
					analiz_level_max.append([0] * len(analiz_max0[g2].tolist()))
				if g == "High":
					analiz_level_max.append(analiz_max0[g2].tolist())
					analiz_level_min.append([0] * len(analiz_min0[g2].tolist()))
				if g == "Low":
					analiz_level_min.append(analiz_min0[g2].tolist())
					analiz_level_max.append([0] * len(analiz_max0[g2].tolist()))
			big_analiz_level_max.append(pd.DataFrame(analiz_level_max).T)
			big_analiz_level_min.append(pd.DataFrame(analiz_level_min).T)
			#print(len(name_keys))
			def list_to_dict(a,b):
			    new_dict={a[i]:b[i] for i in range(len(a))}
			    return new_dict
			
			result = list_to_dict(name_keys,analiz_level_max)
			result2 = list_to_dict(name_keys,analiz_level_min)

			
			with pd.ExcelWriter(pyt_save_zadac + "/" + name[i], engine = 'openpyxl', mode='a') as writer:
				df_min_analizi = pd.DataFrame(result2)
				df_min_analizi.to_excel(writer, sheet_name = "1" )
				df_max_analizi = pd.DataFrame(result)
				df_max_analizi.to_excel(writer, sheet_name = "2"  )

		return big_analiz_level_max,big_analiz_level_min
	BIG_df_max_min = Data_Frame_at_level(return_level,analiz_min0,analiz_max0,name) #возрат MAX и MIN порядок
	print("********")
	print(len(BIG_df_max_min)) #2 мин и макс
	print(len(BIG_df_max_min[0])) #23 задачи
	print(len(BIG_df_max_min[0][0])) # 22 класса
	#print(len(BIG_df_max_min[0][0][0])) # 22 значения для классов e элемента # не имеет значения
	def Neuron_max_min(df_main,df_zadaca):
		array_df = df_main.values
		zero_matrix = np.zeros((22,63))
		c = []
		c2 = [[1,0]]
		for i in range(len(array_df)):
			g = list(array_df[i])
			g2 = list(zero_matrix[i])
			c += [[g,g2]]
		
		answer = []
		for t in range(len(c)):
			def sigmoid(x):
				return 1/(1+ np.exp(-x))

			traninig_inputs = np.array(c[t])
			traninig_outputs = np.array(c2).T

			np.random.seed(1)
			synaptic_weights = 2 * np.random.random((63,1)) - 1
			for K in range(10000):
				input_layer = traninig_inputs
				outputs = sigmoid(np.dot(input_layer,synaptic_weights))

				err = traninig_outputs - outputs
				addjustment = np.dot( input_layer.T, err * (outputs * (1 - outputs)) )

				synaptic_weights += addjustment
			elemen_t_klass_zadac = []
			for tr in range(len(df_zadaca)):
				ZD = df_zadaca[tr].values
				elemen_t_klass_zadac.append(list(ZD[t]))
			new_inputs = np.array(elemen_t_klass_zadac)
			outputs = sigmoid(np.dot(new_inputs, synaptic_weights))
			answer.append([float(outputs[ir]) for ir in range(len(outputs))])
		cover_to_df = []
		for i in range(len(answer[0])):
			min_df_add_convert = []
			for i2 in range(len(answer)):
				min_df_add_convert += [answer[i2][i]]
			cover_to_df.append(min_df_add_convert)
		print(len(cover_to_df))
		print(cover_to_df[0])
		return cover_to_df

	def Run_neuron_1():
		print(BIG_df_max_min[0])
		gob_max = Neuron_max_min(analiz_max0,BIG_df_max_min[0])
		gob_min = Neuron_max_min(analiz_min0,BIG_df_max_min[1])
		for i in range(len(gob_max)):
			with pd.ExcelWriter(pyt_save_zadac + "/" + name[i], engine = 'openpyxl', mode='a') as writer:
				df_gob_max = pd.DataFrame(gob_max[i], columns = ["Значения max"])
				df_gob_min = pd.DataFrame(gob_min[i], columns = ["Значения min"])
				Con_df_min_max = pd.concat([df_gob_max, df_gob_min],axis = 1)
				Con_df_min_max.to_excel(writer,sheet_name = "3")

	#Run_neuron_1()

	def Neuron_on_DF_at_level(df_main,df_zadaca):
		imena_obsh_pokazat = ["красная",
										"белая",
										"тромбоцит",
										"белок",
										"глюк",
										"биллир",
										"хс",
										"креат и моч",
										"альфа щф",
										"ц реак",
										"аст",
										"алт",
										"ггт",
										"лдг",
										"пш",
										"ионы"]
		pozicia = [0,12,27,33,41,42,45,46,48,50,51,52,53,54,55,56,63]
		array_df = df_main.values
		zero_matrix = np.zeros((22,63))
		eye_matrix = np.eye(44,44)
		eye_matrix = eye_matrix[0:44:2]
		big_outputs_radel_analizov = []
		for t in range(len(imena_obsh_pokazat)):
			g = array_df[0:,pozicia[t]:pozicia[t+1]]
			g2 =zero_matrix[0:,pozicia[t]:pozicia[t+1]]
			g3 = []
			for y in range(len(g)):
				g3 +=([list(g[y]),list(g2[y])]) 
			#print(len(g3))
			#print(len(g3[0]))
			def sigmoid(x):
				return 1/(1+ np.exp(-x))
			traninig_inputs = np.array(g3)
			traninig_outputs = np.array(np.array(eye_matrix)).T
			np.random.seed(1)
			synaptic_weights = 2 * np.random.random((len(g3[0]),22)) - 1
			for K in range(10000):
				input_layer = traninig_inputs
				outputs = sigmoid(np.dot(input_layer,synaptic_weights))

				err = traninig_outputs - outputs
				addjustment = np.dot( input_layer.T, err * (outputs * (1 - outputs)) )

				synaptic_weights += addjustment
			ad_all_zadac = []

			for i in range(len(df_zadaca)):
				df_zadaca1 = df_zadaca[i]
				df_zadaca2 = df_zadaca1.values
				df_zadaca3 = df_zadaca2[0:,pozicia[t]:pozicia[t+1]]
				ad_all_zadac.append(list(df_zadaca3))
			new_inputs = np.array(ad_all_zadac)
			outputs = sigmoid(np.dot(new_inputs, synaptic_weights))
			outputs_all_zadaca = []
			for add in range(len(ad_all_zadac)):
				outputs_all_zadaca.append(list(outputs[add]))
			print(len(outputs_all_zadaca))
			print(len(outputs_all_zadaca[0]))
			big_outputs_radel_analizov.append(outputs_all_zadaca)
		return big_outputs_radel_analizov
	print("BAG")

	def Run_neuron_2(name):
		imena_obsh_pokazat = ["красная",
										"белая",
										"тромбоцит",
										"белок",
										"глюк",
										"биллир",
										"хс",
										"креат и моч",
										"альфа щф",
										"ц реак",
										"аст",
										"алт",
										"ггт",
										"лдг",
										"пш",
										"ионы"]
		gob_max_ = Neuron_on_DF_at_level(analiz_max0,BIG_df_max_min[0])
		gob_min_ = Neuron_on_DF_at_level(analiz_min0,BIG_df_max_min[1])
		
	Run_neuron_2(name)


#######################загрузочные DataFrame
def run_for_zadac_analizi():
	data_frame_all_zadac_analizi = []
	for i in range(len(a)):
		name_zadaca = pyt_zagruzka + '/' + a[i]
		df = pd.read_excel(name_zadaca,sheet_name = 1)
		data_frame_all_zadac_analizi.append(df)
	return data_frame_all_zadac_analizi
Analiz = run_for_zadac_analizi()
Analizi_run = Analizi(Analiz,a,analiz_min0,analiz_max0)
