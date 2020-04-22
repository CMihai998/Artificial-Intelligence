from time import time

from Configuration import Configuration
from Problem import Problem
from Controller import Controller
class UI:
    def __init__(self, size):
        self._initialConfig = Configuration(size)
        self._problem = Problem(self._initialConfig)
        self._controller = Controller(self._problem)

    def printMenu(self):
        print("\n---------------------\n" +
              "0 - exit\n" +
              "1 - solve with DFS\n" +
              "2 - solve with Greedy\n" +
              "3 - give new size\n")

    def  run(self):
        runM = True
        self.printMenu()
        while runM:

            command = int(input(">"))
            if command == 0:
                runM = False
            elif command == 1:
                self.solveDFS()
            elif command == 2:
                self.solveBestFS()
            elif command == 3:
                self.reconfigure()
            self.printMenu()


    def solveDFS(self):
        startClock = time()
        print(self._controller.DFS(self._problem.getRoot()))
        print("execution time = ", time() - startClock, " seconds")

    def solveBestFS(self):
        startClock = time()
        print(self._controller.Greedy(self._problem.getRoot()))
        print("execution time = ", time() - startClock, " seconds")

    def reconfigure(self):
        size = 5
        try:
            print("Input the size of the board and number of queens (implicit 5)")
            size = int(input("size = "))
        except:
            print("Invalid input, implicit value is still in place")
        self._initialConfig = Configuration(size)
        self._problem = Problem(self._initialConfig)
        self._controller = Controller(self._problem)


ui = UI(5)
ui.run()
