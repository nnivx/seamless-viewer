#!/usr/bin/env python3

import pygame
import re, operator
import sys


def list_files(path):
	"""List files in directory"""
	from os import listdir
	from os.path import isfile, join
	return [f for f in listdir(path) if isfile(join(path, f))]

class Canvas(object):
	"""A virtual canvas"""

	def __init__(self, regex, directory='.', gap=0):
		self.__r = re.compile(regex)
		self.directory = directory
		self.gap = gap
		self.reload()

	def reload(self):
		self.images = {path: pygame.image.load(path).convert() for path in sorted(filter(self.__r.search, list_files(self.directory)))}

		# supports variable width
		maxw, maxh = 0, 0
		for surf in self.images.values():
			w, h = surf.get_size()
			if w > maxw: maxw = w
			maxh = maxh + h + self.gap
		self.size = (maxw, maxh)
		
		y = 0
		surf = pygame.Surface(self.size)
		for k, image in sorted(self.images.items())	:
			size = image.get_size()
			offset_x = (maxw - size[0])/2
			rect = surf.blit(image, (offset_x, y))
			y = y + size[1] + self.gap
		self.surface = surf
	
	def export(self, filename):
		pygame.image.save(self.surface, filename)

# START	

def start_viewer(display_size, regex, gap=0, margin=10, directory='.'):
	pygame.init()
	display_size = tuple(display_size)
	screen = pygame.display.set_mode(display_size)
	margin = display_size[0]/margin
	pygame.display.set_caption('Simple Viewer v0.1', 'Simple Viewer')
	
	canv = Canvas(regex, directory=directory, gap=gap)
	scale = (display_size[0] - margin)/canv.size[0]
	max_scroll_y = scale*canv.size[1]-display_size[1]
	
	# this is slow since we load the entire canvas into a single surface
	# and scale the entire thing when we change scale ^^
	# it's a quick and dirty method and well just optimize later

	img = pygame.transform.smoothscale(canv.surface, [int(scale*canv.size[0]), int(scale*canv.size[1])])

	held_state = (False, 0, 0, 0)
	done = False
	scroll_y = 0

	clock = pygame.time.Clock()
	while not done:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				done = True
			if e.type == pygame.MOUSEBUTTONDOWN:
			# scroll
				if e.button == 4: scroll_y = max(scroll_y - 50, 0)
				if e.button == 5: scroll_y = min(scroll_y + 50, max_scroll_y)
			# grab
				if e.button == 1:
					held_state = (True, e.pos[0], e.pos[1], scroll_y)
			if e.type == pygame.MOUSEBUTTONUP:
				held_state = (False, 0, 0, 0)
			if held_state[0] and e.type == pygame.MOUSEMOTION:
				scroll_y = held_state[3] - (e.pos[1] - held_state[2])
				if (scroll_y < 0): scroll_y = 0
				elif(scroll_y > max_scroll_y): scroll_y = max_scroll_y
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_s:
					canv.export('save.png')
					print('Image saved.')
	
		re = screen.blit(img, (margin/2, -scroll_y))

		pygame.display.update(re)
		clock.tick(30)

	pygame.quit()


if __name__ == '__main__':
	args = len(sys.argv)	
	if args < 2:
		print('Must at provide regex for filename filter')
		quit()
	
	if sys.argv[1] == '--help':
		print('Usage: simpleviewer regex [width height gap margin directory]')
		quit()

	regex = sys.argv[1]

	extra = [(1000, 600), 0, 10, '.']
	if args >= 4: extra[0] = (int(sys.argv[2]), int(sys.argv[3]))
	if args >= 5: extra[1] = int(sys.argv[4])
	if args >= 6: extra[2] = int(sys.argv[5])
	if args >= 7: extra[3] = sys.argv[6]
	
	start_viewer(extra[0], regex, extra[1], extra[2], extra[3])


