from collections import defaultdict
import numpy as np


def probability_generator(s, t):
    prob = [(Actions[t], 0.7)]
    if t in 'aNorth':
        prob.append((Actions['cEast'], 0.1))
        prob.append((Actions['dWest'], 0.1))
        prob.append((Actions['bSouth'], 0.1))
    elif t in 'bSouth':
        prob.append((Actions['cEast'], 0.1))
        prob.append((Actions['dWest'], 0.1))
        prob.append((Actions['aNorth'], 0.1))
    elif t in 'cEast':
        prob.append((Actions['aNorth'], 0.1))
        prob.append((Actions['bSouth'], 0.1))
        prob.append((Actions['dWest'], 0.1))
    else:
        prob.append((Actions['aNorth'], 0.1))
        prob.append((Actions['bSouth'], 0.1))
        prob.append((Actions['cEast'], 0.1))
    for d, probability in prob:
        next_cell = s[0]+d[0], s[1]+d[1]
        if next_cell not in States:
            next_cell = s
        yield next_cell, probability


def get_pos(position, direc, length):
    (pos_row, pos_col) = position
    final_row, final_col = -1, -1
    if direc == "aNorth":
        final_row, final_col = pos_row-1, pos_col
    elif direc == "bSouth":
        final_row, final_col = pos_row+1, pos_col
    elif direc == "cEast":
        final_row, final_col = pos_row, pos_col+1
    else:
        final_row, final_col = pos_row, pos_col-1
    if final_row < 0 or final_row >= length:
        final_row = pos_row
    if final_col < 0 or final_col >= length:
        final_col = pos_col
    return final_row, final_col


def turn_left(pos1, direct1, matrix1):
    if direct1 == "aNorth":
        return get_pos(pos1, "dWest", matrix1)
    elif direct1 == "bSouth":
        return get_pos(pos1, "cEast", matrix1)
    elif direct1 == "cEast":
        return get_pos(pos1, "aNorth", matrix1)
    else:
        return get_pos(pos1, "bSouth", matrix1)


def turn_right(pos2, direct2, matrix2):
    if direct2 == "aNorth":
        return get_pos(pos2, "cEast", matrix2)
    elif direct2 == "bSouth":
        return get_pos(pos2, "dWest", matrix2)
    elif direct2 == "cEast":
        return get_pos(pos2, "bSouth", matrix2)
    else:
        return get_pos(pos2, "aNorth", matrix2)


def turn_opposite(pos3, direct3, matrix3):
    if direct3 == "aNorth":
        return get_pos(pos3, "bSouth", matrix3)
    elif direct3 == "bSouth":
        return get_pos(pos3, "aNorth", matrix3)
    elif direct3 == "cEast":
        return get_pos(pos3, "dWest", matrix3)
    else:
        return get_pos(pos3, "cEast", matrix3)


def expected_utility(a1, s1, value, size):
    (rr1, cc1) = s1
    neighbours = {
        (rr1, min(cc1 + 1, size - 1)),
        (rr1, max(cc1 - 1, 0)),
        (max(rr1 - 1, 0), cc1),
        (min(rr1 + 1, size - 1), cc1)
    }
    return np.float64(sum(np.float64(P[s1, a1, n1] * value[n1]) for n1 in neighbours))


with open('input.txt', 'r') as inp, open('output.txt', 'w') as out:
    grid = int(inp.readline().strip())
    cars_count = int(inp.readline().strip())
    obstacles_count = int(inp.readline().strip())
    obstacles, cars, ends = [], [], []
    for x in range(obstacles_count):
        (c, r) = map(int, inp.readline().strip().split(","))
        obstacles.append((r, c))
    for y in range(cars_count):
        (c, r) = map(int, inp.readline().strip().split(","))
        cars.append((r, c))
    for z in range(cars_count):
        (c, r) = map(int, inp.readline().strip().split(","))
        ends.append((r, c))

    States = []
    for x in range(grid):
        for y in range(grid):
            States.append((x, y))

    Actions = {'aNorth': (-1, 0), 'bSouth': (1, 0), 'cEast': (0, 1), 'dWest': (0, -1)}

    Rewards = {s: -1 for s in States}

    for (r, c) in obstacles:
        Rewards[(r, c)] -= 100

    gamma = 0.9
    epsilon = 0.1
    error = np.float64(epsilon * (1 - gamma) / gamma)
    for i in range(len(cars)):

        (r, c) = ends[i]
        R = Rewards.copy()
        R[(r, c)] += 100

        P = defaultdict(int)

        for s in States:
            if s in [ends[i]]:
                continue
            for a in Actions:
                for n, x in probability_generator(s, a):
                    P[s, a, n] = np.float64(P[s, a, n] + x)

        V, V1 = {}, {s: R[s] for s in States}

        while True:
            V = V1.copy()
            delta = 0
            for s in States:
                sums = []
                for a in Actions:
                    (r1, c1) = s
                    neighbors = {
                        (r1, min(c1 + 1, grid - 1)),
                        (r1, max(c1 - 1, 0)),
                        (max(r1 - 1, 0), c1),
                        (min(r1 + 1, grid - 1), c1)
                    }
                    total = 0
                    for n in neighbors:
                        total = np.float64(total + (P[s, a, n] * V[n]))
                    sums.append(total)
                V1[s] = np.float64(R[s] + gamma * max(sums))
                delta = np.float64(max(delta, abs(V1[s] - V[s])))
            if delta < error:
                break

        pi = {s: max(sorted(Actions), key=lambda a1: expected_utility(a1, s, V, grid)) for s in States}

        final_reward = 0
        
        for j in range(10):
            pos = cars[i]
            np.random.seed(j)
            swerve = np.random.random_sample(1000000).astype(np.float64)
            k, total_reward = 0, 0
            if pos == ends[i]:
                total_reward = 100
            while pos != ends[i]:
                direction = pi[pos]
                move = pos
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = turn_opposite(pos, direction, grid)
                        else:
                            move = turn_right(pos, direction, grid)
                    else:
                        move = turn_left(pos, direction, grid)
                else:
                    move = get_pos(pos, direction, grid)
                total_reward += R[move]
                k += 1
                pos = move
            final_reward += total_reward
        out.write(str(final_reward // 10))
        out.write("\n")