#solves a travelling salesman problem starting with an affinity matrix.
import tsp
import random
from math import sqrt
from math import exp
import numpy

def tour_sum_affinities(aff,tour):
    total = 0 
    n = len(tour)
    for i in range(n):
        j=(i+1)%n
        ii=tour[i]
        jj=tour[j]
        total+=aff[ii,jj]
    return total

def test_solve_anneal():
    n = 50
    coords = {}
    for i in range(0,n-1):
        coords[i,0] = random.random()
        coords[i,1] = random.random()

    affs = {}
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx,dy=x1-x2,y1-y2
            dist=sqrt(dx*dx + dy*dy)
            affs[i,j] = exp(-dist)
    
    iterations, score, best = solve_anneal(affs)
    return iterations, score, best

def solve_anneal(aff):
    objective_function=lambda tour: tour_sum_affinities(aff,tour)
    init_function=lambda: tsp.init_random_tour(sqrt(len(aff)))
    move_operator=tsp.reversed_sections

    #suggested parameters for simulated annealing:
    start_temp = 10.0
    max_iterations = 5000
    alpha = .001**(1/max_iterations)

    from sa import anneal
    iterations,score,best=anneal(init_function,move_operator,objective_function,max_iterations,start_temp,alpha)
    return iterations,score,best
    
