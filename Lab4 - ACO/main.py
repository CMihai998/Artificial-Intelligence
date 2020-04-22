from copy import deepcopy

import numpy

from controller.controller import Controller
from models.ant import Ant


class UI:
    def __init__(self):
        self._controller = None

    def run(self):
        print("Will print best solution found atm with current fitness (the lower, the better) + \n + (Values in paranthesis are recommended values)")
        individualSize = int(input("Solution size>"))
        populationSize = int(input("Population size>"))
        iterationsAllowed = int(input("Iterations allowed>"))
        alpha = float(input("alpha (1.3)>"))
        beta = float(input("beta (0.4)>"))
        q0 = float(input("q0 (0.5)>"))
        rho = float(input("rho (0.05)>"))
        self._controller = Controller(individualSize, populationSize)
        sol = self._controller.ACO(iterationsAllowed, alpha, beta, q0, rho)
        print("SOLUTION:")
        print(sol)
        print(sol.fitness())

ui = UI()
ui.run()

