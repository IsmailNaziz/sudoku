from itertools import product
import copy
from random import choice
from time import sleep
import os
from math import sqrt


class GridManager(object):
	"""docstring for GameManager"""

	

	def __init__(self, size_x=9, size_y=9):
		self.size = size_x
		self.box_size = int(sqrt(self.size)) # edge of the square
		self.grid = self._init_grid()
		self.boxes = self._generate_boxes() # key index of the box : value points in the box
		self.ref = set([str(i) for i in range(1,self.size+1)])
		self.valid = True


	def _generate_boxes(self):
		boxes = {}
		size = self.box_size
		for num in range(size**2):
			translate_i, translate_j = num//size*size, num%size*size
			boxes[str(num)] = [(i + translate_i, j + translate_j) for i,j in product(range(size), range(size))]
		return boxes

	def print_check_boxes(self):
		backup_grid = copy.deepcopy(self.grid)
		for box, indexes in self.boxes.items():
			for index in indexes: 
				self.replace_index_value(index, box)
		print(self)
		self.grid = backup_grid


	def snail_browse(self, min_i, max_i, min_j, max_j, display_mode=False):
		row_i, col_j = min_i, min_j
		
		# snail browse

		# first row left to right
		while col_j < max_j:
			self.replace_with_random_available_value((row_i, col_j))
			col_j += 1
			if display_mode:
				self.slow_display()
			
		# last col top to bot
		while row_i < max_i:
			self.replace_with_random_available_value((row_i, col_j))
			row_i += 1
			if display_mode:
				self.slow_display()

		# last row right to left
		while col_j > min_j:
			self.replace_with_random_available_value((row_i, col_j))
			col_j -= 1
			if display_mode:
				self.slow_display()

		# first col bot to top
		while row_i > min_i:
			self.replace_with_random_available_value((row_i, col_j))
			row_i -= 1
			if display_mode:
				self.slow_display()

	def _fill_grid_snail(self, display_mode=False):
		# init
		nb_rows, nb_cols = len(self.grid), len(self.grid[0])		
		row_i, col_j = 0, 0
		min_i, max_i = 0, nb_rows-1
		min_j, max_j = 0, nb_cols-1

		if nb_rows%2==0:
			while max_i >= min_i+1 and max_j >= min_j+1: # one condition is enough
				self.snail_browse(min_i, max_i, min_i, max_i, display_mode)
				max_i -= 1
				max_j -= 1
				min_i += 1
				min_j += 1
		else:
			middle_index = nb_rows//2, nb_cols//2
			while max_i >= min_i+1 and max_j >= min_j+1: # one condition is enough
				self.snail_browse(min_i, max_i, min_i, max_i, display_mode)
				max_i -= 1
				max_j -= 1
				min_i += 1
				min_j += 1
			self.replace_with_random_available_value(middle_index)
			if display_mode:
				self.slow_display()
	
	def _fill_grid_line_by_line(self, display_mode=False):
		nb_rows, nb_cols = len(self.grid), len(self.grid[0])
		for row_i in range(nb_rows):
			for col_j in range(nb_cols):
				self.replace_with_random_available_value((row_i, col_j))
				if display_mode:
						self.slow_display()

	def _fill_grid_box_by_box(self, display_mode=False):
		for box, indexes in self.boxes.items():
			for index in indexes:
				self.replace_with_random_available_value(index)
				if display_mode:
						self.slow_display()


	def slow_display(self):
		print(self)
		sleep(0.2)
		os.system('cls||clear')

	def replace_with_random_available_value(self, actual_index):
		random_value = self.pick_random_from_set(self.get_availabilities(actual_index))
		self.replace_index_value(actual_index, random_value)

	@classmethod
	def pick_random_from_set(cls, this_set):
		return choice(tuple(this_set))
		 

	def _init_grid(self):
		return[[' ' for i in range(self.size)] for j in range(self.size)]

	def _reset_grid(self):
		self.grid = self._init_grid()


	def get_availabilities(self, actual_index):
		list_sets = [self._get_row_availability(actual_index),
					 self._get_col_availability(actual_index),
					 self._get_box_availability(actual_index)]
		if set.intersection(*list_sets):
			return set.intersection(*list_sets)

		else: 
			self.valid = False
			return {'E'}

	@classmethod
	def debug_print(cls, iter_to_display):
		print("------------------------------------------------------")
		print("------------------------------------------------------")
		for elem in iter_to_display:
			if isinstance(elem, list):
				for sub_elem in elem:
					print(sub_elem)
					print("------------------------------------------------------")
					print("------------------------------------------------------")
			else:
				print(elem)
				print("------------------------------------------------------")
				print("------------------------------------------------------")
	 
	def _get_row_availability(self, actual_index):
		row_indexes = [(i, actual_index[1]) for i in range(len(self.grid))]
		not_available_values = self.get_values_from_indexes(row_indexes)
		return self._complementary_set(not_available_values) 

	def _get_col_availability(self, actual_index):
		column_indexes = [(actual_index[0], i) for i in range(len(self.grid))]
		not_available_values = self.get_values_from_indexes(column_indexes)
		return self._complementary_set(not_available_values) 

	def _get_box_availability(self, actual_index):
		actual_box = self.get_box(actual_index)
		not_available_values = self.get_values_from_indexes(self.boxes[actual_box])
		return self._complementary_set(not_available_values)

	def get_box(self, actual_index):
		for box, indexes in self.boxes.items():
			if actual_index in indexes: 
				return box

	def get_values_from_index(self, index):
		return self.grid[index[0]][index[1]]

	def get_values_from_indexes(self, list_index):
		return set([self.get_values_from_index(index) for index in list_index if self.get_values_from_index(index)!= ' '])

	def replace_index_value(self, index, value):
		self.grid[index[0]][index[1]] = value

	def _complementary_set(self, this_set):
		return self.ref - this_set

	def __str__(self):
		rows_display = ['|'.join(row) for row in self.grid]
		return '\n'.join(rows_display)

	def diplay_fill_in(self):
		return self._generate_grid_to_fill(display_mode=True)


if __name__ == '__main__':


	def success_rate(size_x, size_y, total_attempt, *args):
		if len(args) == 0:
			return 'no method to evaluate'

		if len(args)>1:
			for method_name in args:
				nb_success, nb_fail = 0, 0
				for i in range(total_attempt):
					GM = GridManager(size_x, size_y)
					method_to_evaluate = getattr(GridManager, method_name)
					method_to_evaluate(GM)
					if GM.valid:
						nb_success+=1
					else:
						nb_fail+=1
				print(r'le % de reussite de {} est de {}% pour une matrice de taille {}x{}'\
						.format(method_name, round((nb_success/total_attempt)*100,2), size_x, size_y))

	evaluate = False
	display = True
	if display:
		size_x, size_y = 4, 4
		GM = GridManager()
		GM._fill_grid_snail(display_mode=True)
		GM._reset_grid()
		GM._fill_grid_line_by_line(display_mode=True)
		GM._reset_grid()
		GM._fill_grid_box_by_box(display_mode=True)
	if evaluate:
		method_list = ['_fill_grid_snail', '_fill_grid_line_by_line', '_fill_grid_box_by_box']
		test_1 = (4, 4, 1000, *method_list)
		test_2 = (9, 9, 1000, *method_list)

		success_rate(*test_1)
		success_rate(*test_2)
