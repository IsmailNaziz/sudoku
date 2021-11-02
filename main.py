from itertools import product, chain
import copy
from random import choice
from time import sleep

class GridManager(object):
	"""docstring for GameManager"""

	REF = set([str(i) for i in range(1,10)])

	def __init__(self, size_x=9, size_y=9):
		self.grid = self._init_grid(size_x, size_y)
		self.box_size = 3 # edge of the square
		self.boxes = self._generate_boxes() # key index of the box : value points in the box


	def _generate_boxes(self):
		boxes = {}
		for num in range(self.box_size**2):
			translate_i, translate_j = num//3*3, num%3*3
			boxes[str(num)] = [(i + translate_i, j + translate_j) for i,j in product(range(3), range(3))]
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

	def _fill_grid(self, display_mode=False):
		# init
		nb_rows, nb_cols = len(self.grid), len(self.grid[0])		
		row_i, col_j = 0, 0
		min_i, max_i = 0, nb_rows-1
		min_j, max_j = 0, nb_cols-1

		while max_i >= min_i and max_j >= min_j: # one condition is enough
			self.snail_browse(min_i, max_i, min_i, max_i, display_mode)
			max_i -= 1
			max_j -= 1
			min_i += 1
			max_i += 1
			
	def slow_display(self):
		print(self)
		sleep(0.2)

	def replace_with_random_available_value(self, actual_index):
		random_value = self.pick_random_from_set(self.get_availabilities(actual_index))
		self.replace_index_value(actual_index, random_value)

	@classmethod
	def pick_random_from_set(cls, this_set):
		return choice(tuple(this_set))
		 

	def _init_grid(self, size_x, size_y):
		return[[' ' for i in range(size_y)] for j in range(size_x)]


	def get_availabilities(self, actual_index):
		list_sets = [self._get_row_availability(actual_index),
					 self._get_col_availability(actual_index),
					 self._get_box_availability(actual_index)]
		return set(chain(*list_sets))

	def _get_row_availability(self, actual_index):
		row_indexes = [(i, actual_index[1]) for i in range(9)]
		not_available_values = self.get_values_from_indexes(row_indexes)
		return self._complementary_set(not_available_values) 

	def _get_col_availability(self, actual_index):
		column_indexes = [(actual_index[0], i) for i in range(9)]
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

	@classmethod
	def _complementary_set(cls, this_set):
		return cls.REF - this_set

	def __str__(self):
		rows_display = ['|'.join(row) for row in self.grid]
		return '\n'.join(rows_display)

	def diplay_fill_in(self):
		return self._generate_grid_to_fill(display_mode=True)


if __name__ == '__main__':
	GM = GridManager()
	GM._fill_grid(display_mode=True)