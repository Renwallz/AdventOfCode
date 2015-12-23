#!/usr/bin/python3
import re

# Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
parser = re.compile(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')
deers = []

TOTAL_TIME = 2503

class reindeer(object):
    def __init__(self, name, speed, run_time, rest_time):
        self.name = name
        self.speed = int(speed)
        self.run_time = int(run_time)
        self.rest_time = int(rest_time)

        self.total_time = self.run_time + self.rest_time
        self.current_distance = 0
        self.score = 0

    def run(self, current_tick):
        if (current_tick % self.total_time) < self.run_time:
            self.current_distance += self.speed
        return self.current_distance


with open('day14.in') as f:
    for line in f:
        deers.append(reindeer(*parser.match(line).groups()))

for i in range(TOTAL_TIME):
    for deer in deers:
        deer.run(i)
    pos = sorted(deers, key=lambda x: x.current_distance, reverse=True)
    print(pos)
    current_furtherest_distance = pos[0].current_distance

    for deer in pos:
        if deer.current_distance != current_furtherest_distance:
            break
        deer.score += 1

for deer in deers:
    print("{} got {} and a score of {}".format(deer.name, deer.current_distance, deer.score))