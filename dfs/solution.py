"""
    This module provides a solution for transportation problem in LA
"""
#!/usr/bin/env python


#Author: Divya Ramesha

import itertools as it

class Transportation(object):
    """
        A Transportation class to solve real world transportation problem in LA.

        It places police officers in streets where there are maximum chances of accidents
    """

    def __init__(self, point_count, officers, final_result):
        self.point_count = point_count
        self.officers = officers
        self.final_result = final_result

    def can_place_police_officer(self, xp2, yp2):
        """
            This function checks whether we can place police officer in (x, y) without any conflicts
            Args:
                xp2: x co-ordinate in grid
                yp2: y co-ordinate in grid
        """
        for key, val in self.officers.iteritems():
            if ((key == xp2) or (val == yp2) or (abs(key - xp2) == abs(val - yp2))):
                return False
        return True

    def place_police_officers(self, next_police, rows, grid):
        """
            This function places the police officers in rows of grid
            Args:
                next_police: next police officer to place
                rows: list showing rows in which police officers will be placed
                grid: matrix grid
        """
        for i in xrange(grid):
            if self.can_place_police_officer(rows[next_police], i):
                self.officers[rows[next_police]] = i
                if len(self.officers) == len(rows):
                    total = 0
                    for x_point in self.officers:
                        point = str(x_point) + "," + str(self.officers[x_point])
                        total += self.point_count[point]
                    if total > self.final_result:
                        self.final_result = total
                    del self.officers[rows[next_police]]
                if (next_police + 2) <= len(rows):
                    self.place_police_officers(next_police+1, rows, grid)
                if rows[next_police] in self.officers:
                    del self.officers[rows[next_police]]

if __name__ == "__main__":

    with open('input.txt', 'r') as input_file, open('output.txt', 'w') as output_file:

        TRANSPORT_INSTANCE = Transportation(dict(), dict(), 0)
        GRID_COUNT = int(input_file.readline().strip())
        POLICE_COUNT = int(input_file.readline().strip())
        SCOOTER_COUNT = input_file.readline()
        for x in xrange(GRID_COUNT):
            for y in xrange(GRID_COUNT):
                p = str(x)+","+str(y)
                TRANSPORT_INSTANCE.point_count[p] = 0
        for line in input_file:
            line = line.strip()
            TRANSPORT_INSTANCE.point_count[line] += 1
        for comb in it.combinations([num for num in xrange(GRID_COUNT)], POLICE_COUNT):
            TRANSPORT_INSTANCE.officers = dict()
            TRANSPORT_INSTANCE.place_police_officers(0, list(comb), GRID_COUNT)
        output_file.write(str(TRANSPORT_INSTANCE.final_result))
