import math
import random
from copy import deepcopy

from tools import Point, Routine

points = Point.from_sequence([[565, 575], [25, 185], [345, 750], [945, 685], [845, 655], [880, 660],
                              [25, 230], [525, 1000], [580, 1175], [650, 1130], [1605, 620], [1220, 580], [1465, 200],
                              [1530, 5],
                              [845, 680], [725, 370]], offset=1)
routine = Routine(points)


def permute(routine, current_index=0):
    if current_index == len(routine):
        yield routine

    else:
        for i in range(current_index, len(routine)):
            routine.exchange(current_index, i)
            yield from permute(routine, current_index + 1)
            routine.exchange(current_index, i)


class SimulatedAnnealing:
    def __init__(self, initial_route: Routine, temperature, cooling_rate, min_temperature):
        self.current_route = initial_route
        self.best_route = deepcopy(initial_route)
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature

    def anneal(self):
        while self.temperature > self.min_temperature:
            new_route = deepcopy(self.current_route)

            # exchange randomly
            i, j = random.sample(range(len(new_route)), 2)
            new_route.exchange(i, j)

            # calc cost
            current_cost = self.current_route.length()
            new_cost = new_route.length()
            cost_difference = current_cost - new_cost

            # accepting the new result?
            if cost_difference > 0 or math.exp(cost_difference / self.temperature) > random.random():
                self.current_route = new_route
                if new_cost < self.best_route.length():
                    self.best_route = new_route

            # decrease the temperature
            self.temperature *= (1 - self.cooling_rate)

        return self.best_route


def annealing(epochs=100):
    final_best_route = deepcopy(routine)
    for i in range(epochs):
        print(f"Running epoch: {i}")
        sa = SimulatedAnnealing(routine, 10000, 0.003, 1)
        best_route = sa.anneal()
        if best_route.length() < final_best_route.length():
            final_best_route = deepcopy(best_route)
            print("A new best route is:", final_best_route)
        random.shuffle(routine)

    print("Best route found:\n", [point.name for point in final_best_route])
    print("Length of best route:", final_best_route.length())


def exhaustive_indexing():
    best_route = deepcopy(routine)
    count = 0
    print("length of start route: ", best_route.length())
    for route in permute(routine):
        # print("length of current route: ", route.length())
        count += 1
        if route.length() < best_route.length():
            best_route = deepcopy(route)

    print(best_route)
    print(f"count: {count}")


if __name__ == "__main__":
    annealing()
