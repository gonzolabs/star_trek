#! /usr/bin/env python
'''
A brute force solution to the annoying Star Trek logic problem:
http://io9.com/can-you-solve-this-extremely-difficult-star-trek-puzzle-1667991339
by John Bohannon
14 December 2014
'''

from itertools import permutations

class Person():
	def __init__(self, name):
		self.name = name
		self.fizz = self.tri = 0
		self.hero = self.fear = self

crew_names = ['G', 'P', 'T', 'W', 'D', 'R']
crew = {i:Person(name=i) for i in crew_names}
	
def solve():
	progress = 0
	problem_size = len([i for i in permutations(crew_names)])
	
	# start with Fizzbin rankings
	for fizz_list in permutations(crew_names):

		# keep track of progress
		progress += 1
		if (problem_size - progress) % 10 == 0:
			print problem_size - progress

		# for each Fizzbin ranking permutation, check all Tri-Chess ranking permutations
		for tri_list in permutations(crew_names):

			# let's start by testing the game-only conditions
			if not all([
				# 1. Geordi ranks 2 at Tri-D Chess
				# crew['G'].tri == 2,
				tri_list.index('G') == 1,
				# 2. Picard ranks two positions behind Troi at Fizzbin
				# crew['T'].fizz - crew['P'].fizz == 2,
				fizz_list.index('T') - fizz_list.index('P') == 2,
				# 8. The person who is worst at Fizzbin is better than Troi at Tri-D Chess
				# crew[fizz_list[0]].tri > crew['T'].tri,
				tri_list.index(fizz_list[0]) > tri_list.index('T'),
				# 9. The person ranked number 3 at Tri-D Chess is ranked 4 positions higher than Data at Fizzbin
				# crew[tri_list[2]].fizz - crew['D'].fizz == 4,
				fizz_list.index(tri_list[2]) - fizz_list.index('D') == 4,
				# 11. Riker is ranked 2 lower at Tri-D Chess than the crew member ranked 2 at Fizzbin
				# crew[fizz_list[1]].tri - crew['R'].tri == 2
				tri_list.index(fizz_list[1]) - tri_list.index('R') == 2
				]):
				continue
			
			# those conditions are satisfied, so load the rankings into each crew person
			for n, fizz_player in enumerate(fizz_list):
				crew[fizz_player].fizz = n + 1
			for n, tri_player in enumerate(tri_list):
				crew[tri_player].tri = n + 1

			# build a valid hero graph
			for hero_list in permutations(crew_names):
				# make sure nobody is their own hero
				if any([crew_names[n] == i for n, i in enumerate(hero_list)]):
					continue
				# load the hero into each crew person
				for n, i in enumerate(hero_list):
					crew[crew_names[n]].hero = crew[i]

				# now that we have heroes, let's do fears
				for fear_list in permutations(crew_names):
					# make sure they don't fear themselves
					if any([crew_names[n] == i for n, i in enumerate(fear_list)]):
						continue
					# and make sure no one fears their hero
					if any([hero_list[n] == i for n, i in enumerate(fear_list)]):
						continue
					# load fear into each crew person
					for n, i in enumerate(fear_list):
						crew[crew_names[n]].fear = crew[i]

						# finally, let's test the relationship conditions
						if all([
							# 3. Troi is feared by the person Geordi fears
							crew['T'] == crew['G'].fear.fear,
							# 4. Worf's hero ranks 3 times lower at Tri-D Chess than the crew member who is best at Fizzbin
							3 * crew['W'].hero.tri == crew[fizz_list[-1]].tri,
							# 5. Picard's hero fears Geordi
							crew['P'].hero.fear == crew['G'],
							# 6. Data's hero is not Geordi
							crew['D'].hero != crew['G'],
							# 7. Data is the hero of Riker's hero
							crew['R'].hero.hero == crew['D'],
							# 10. Riker is feared by the person Picard fears and is the hero of Worf's hero
							crew['R'] == crew['P'].fear.fear == crew['W'].hero.hero
							]):
							return True
	return False

solved = solve()
if solved == True:
	print 'person: fizz, tri, hero, fears'
	for c in crew_names:
		print c + ':', crew[c].fizz, crew[c].tri, crew[c].hero.name, crew[c].fear.name
else:
	print "Highly illogical, Captain. There is no solution. Not in this generation, nor the next."
