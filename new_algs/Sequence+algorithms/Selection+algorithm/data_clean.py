import pandas as pd 
import numpy as np

class Data:
	def __init__(self, PATH, task):

		self.ultra_df = pd.read_csv(PATH)	#CREATE ONE IMMUTABLE VERSION OF DATASET
		self.main_df = self.ultra_df.copy() #CREATE ONE ALTERABLE VERSION OF THE DATASET 
		self.task = task	#SPECIFY TASK, I.E. REGRESSION/CLASSIFICATION

		#INITIALIZE VARIABLES 
		self.y_labels = []
		self.target_var = ""
		self.nan_count = 0
		self.nan_list = []
		self.cat_values_dict_array = []
		self.dep = []
		self.essential_cols = []

		#MANY DIFFERENT FUNCTIONS HAVE BEEN CREATED TO HANDLE DIFFERENT FUNCTION CALLS THAT OUGHT TO GO TOGETHER 
		#IN ORDER TO PERFORM A SPECIFIC MAJOR TASK
		self.clean_data()
	
	def clean_data(self):

		#SET_INITIAL_VARS SETS THE VALUES OF VARIABLES USED THROUGHOUT THE CODE. THIS FUNCTION HAS BEEN CALLED MULTIPLE TIMES
		#WHENEVER NUMBER OF COLUMNS OR VALUES CHANGE 
		self.set_initial_vars()
		self.handle_nans()
		self.set_initial_vars()
		self.convert_cat()
		self.sort_with_dependencies()
		self.set_initial_vars()
		self.one_hot_encode()
		self.set_initial_vars()
		

	def set_initial_vars(self):
		#INITIALIZE VARIABLES THAT ARE USED AT MANY PLACES THROUGHOUT THE CODE
		self.dtype_dict = {}
		self.idx2col = {}
		self.col2idx = {}
		self.columns = []
		self.types = []

		self.set_cols()
		self.set_labels()
		self.index()
		self.set_types()
		self.make_type_dict()

	def sort_with_dependencies(self):
		#REMOVE/KEEP COLUMNS W.R.T. A THRESHOLD CORRELATION LEVEL WITH THE TARGET VARIABLE 
		self.make_dependencies()
		self.sift_essential()
		self.remove_non_essential()

	def handle_nans(self):
		#HANDLE NAN VALUES IN BOTH CATEGORICAL AND NUMERIC TYPE COLUMNS 
		self.count_nan()
		self.remove_nan()

	def set_cols(self):
		#SET LIST OF COLUMN NAMES
		self.columns = list(self.main_df.columns)
		
	def set_labels(self):
		#SET Y LABELS AND TARGET VARIABLE NAME
		self.y_labels = self.main_df[self.columns[0]]
		self.target_var = self.columns[0]

	def index(self):
		#CREATE 2 DICTIONARIES, MAPPING COL INDEX TO COL NAME AND VICE VERSA
		for i in range(len(self.columns)):
			self.idx2col[i] = self.columns[i]
			self.col2idx[self.columns[i]] = i

	def set_types(self):
		#SET LIST OF DTYPES FOR EACH COLUMN
		self.types = list(self.main_df.dtypes)
		#print(self.types)

	def make_type_dict(self):
		#CREATE DICTIONARY TO MAP COLUMN TO RESPECTIVE DTYPE
		self.dtype_dict = {self.columns[i]:self.types[i] for i in range(len(self.columns))}

	def convert_cat(self):
		#CONVERT CATEGORICAL DATA TO NUMERIC DATA BY INDEXING CATEGORIES WITHIN EVERY CATEGORICAL COLUMN
		for i in range(len(self.dtype_dict)):
			if self.dtype_dict[self.idx2col[i]] == np.dtype('O'):
				self.cat2numeric(i)

	def cat2numeric(self, col_idx):
		#CONVERT CATEGORICAL DATA TO INDEXED NUMERIC DATA
		unq = list(self.main_df[self.idx2col[col_idx]].unique())
		temp_dict = {unq[i-1]:i for i in range(1, len(unq)+1)}

		self.main_df[self.idx2col[col_idx]] = self.main_df[self.idx2col[col_idx]].replace(temp_dict)
		temp_dict["NAME"] = self.idx2col[col_idx]
		self.cat_values_dict_array.append(temp_dict)

	def one_hot_encode(self):
		#ONE HOT ENCODE CATEGORICAL COLUMNS THAT HAVE 2 <= NUMBER OF CATEGORIES <= 3 
		for col in self.columns:
			count = self.main_df[col].unique()
			if len(count) <= 3 and len(count) > 1 and col!=self.columns[0]:
				self.main_df = pd.concat([self.main_df, pd.get_dummies(self.main_df[col], prefix = col)], axis = 1).drop(col, axis = 1)

	def make_dependencies(self):
		#CALCULATE CORRELATION OF ALL COLS W.R.T. TARGET VAR
		self.dep = self.main_df.corr().values.tolist()[0]
		self.dep_total = self.main_df.corr()

	def sift_essential(self):
		#SIFT FOR ONLY COLUMNS THAT HAVE CORR >= 0.04 OR CORR<= -0.-04 W.R.T. TARGET VAR
		self.essential_cols = [self.idx2col[i] for i in range(len(self.dep)) if self.dep[i] >= 0.04 or self.dep[i] <= -0.04]
		
	def remove_non_essential(self):
		#REMOVE COLUMNS FROM DATAFRAME THAT ARENT ESSENTIAL
		df_temp = self.main_df.copy()
		non_ess = [self.columns[i] for i in range(len(self.columns)) if self.columns[i] not in self.essential_cols]
		for i in range(len(non_ess)):
			df_temp = df_temp.drop([non_ess[i]], axis = 1)

		self.main_df = df_temp.copy()

	def count_nan(self):
		#COUNT NANS IN EVERY COL, CREATE LIST OF COLS WITH NANS
		self.nan_count = list(self.main_df.isna().sum())
		self.nan_list = [self.idx2col[i] for i in range(len(self.nan_count)) if self.nan_count[i] > 0]

	def remove_nan(self):
		#HANDLE NANS FOR BOTH NUMERIC COLUMNS AND CATEGORICAL COLUMNS
		self.handle_numeric_nans()
		self.handle_cat_nans()
						
	def handle_numeric_nans(self):
		#HANDLE NUMERIC NANS BY IMPUTING MEAN VALUES ON A PER-CLASS AND PER-COLUMN BASIS IF CLASSIFICATION AND ON ONLY A PER-COLUMN BASIS IF CLASSIFICATION
		if self.task == 'classification':
			classes, classwise_mean = self.calculate_classwise_mean()
			classwise_frames = [self.main_df[self.main_df[self.columns[0]] == classes[i]] for i in range(len(classes))]

			for i in range(len(classwise_frames)):
				for col in self.nan_list:
					if self.dtype_dict[col] != np.dtype('O'):
						classwise_frames[i] = classwise_frames[i].fillna({col:classwise_mean[classes[i]][col]})

			df3 = pd.DataFrame([])
			for i in range(len(classwise_frames)):
				df3 = pd.concat([df3, classwise_frames[i]])

			self.main_df = df3.sample(frac = 1).reset_index(drop = True)
			self.set_labels()

		elif self.task == 'regression':
			colwise_mean = self.calculate_columnwise_mean()
			for col in self.nan_list:
				if self.dtype_dict[col] != np.dtype('O'):
					self.main_df[col] = self.main_df[col].fillna(colwise_mean[col])


	def calculate_classwise_mean(self):
		#CALCULATE CLASSWISE MEANS FOR IMPUTATION
		classes = self.y_labels.unique().tolist()
		classwise_mean = {}
		for c in classes:
			temp = self.main_df[self.main_df[self.columns[0]] == c]
			classwise_mean[c] = {self.columns[i]: temp[self.columns[i]].fillna(0).values.mean() for i in range(len(self.columns)) if self.dtype_dict[self.columns[i]] != np.dtype('O')}
		return classes, classwise_mean

	def calculate_columnwise_mean(self):
		#CALCULATE COLUMNWISE MEANS FOR IMPUTATION
		colwise_mean = {}
		temp = self.main_df.copy()
		colwise_mean = {self.columns[i]:temp[self.columns[i]].fillna(0).values.mean() for i in range(len(self.columns)) if self.dtype_dict[self.columns[i]] != np.dtype('O')}
		return colwise_mean 


	def handle_cat_nans(self):
		#HANDLE CATEGORICAL NANS BY CREATING MISSING VALUE IN COLUMN AS A CATEGORY ON ITS OWN AS 'MISSING_'+COL NAME IF CLASSIFICATION
		if self.task == 'classification':
				for col in self.nan_list:
					if self.dtype_dict[col] == np.dtype('O'):
						self.main_df[col] = self.main_df[col].fillna("Missing_"+col)

data = Data("D:/Machine Learning Datasets/titanic/train.csv", "regression")
print(data.main_df)