class MaxSum(object):
    def __init__(self, input1, dic1, limit1, sums1, max1, values1):
        self.input = input1
        self.limit = limit1
        self.dic = dic1
        self.sums = sums1
        self.max = max1
        self.values = values1

    def check_whether_we_can_pick_app(self, app1):
        temp = {z: 0 for z in range(7)}
        spaces = self.limit / 7
        days_list = []
        for v in self.input:
            if v[0] in self.values:
                days_list.append(v[1])
        for days_l in days_list:
            for index, val in enumerate(days_l):
                temp[index] += int(val)
        if self.dic[0] + temp[0] + int(app1[0]) <= spaces and self.dic[1] + temp[1] + int(app1[1]) <= spaces and self.dic[
            2] + temp[2] + int(app1[2]) <= spaces and self.dic[3] + temp[3] + int(app1[3]) <= spaces and self.dic[4] + \
                temp[4] + int(app1[4]) <= spaces and self.dic[5] + temp[5] + int(app1[5]) <= spaces and self.dic[6] + \
                temp[6] + int(app1[6]) <= spaces:
            return True
        return False

    def collect_sums(self, n, x):
        for num in range(x, len(self.input)):
            if self.check_whether_we_can_pick_app(self.input[num][1]):
                sum_so_far = n + get_count_for_week(self.input[num][1])
                if sum_so_far <= self.limit:
                    self.values.append(self.input[num][0])
                    if sum_so_far >= self.max and len(self.values) >= 1:
                        self.max = sum_so_far
                        self.sums[self.max] = self.sums.get(self.max, [])
                        self.sums[self.max].append(self.values)
                    self.collect_sums(sum_so_far, num + 1)
        self.values = self.values[:-1]


def get_count_for_week(str_week):
    t = 0
    for dy in str_week:
        t += int(dy)
    return t


def can_we_add_app_to_pool(required1, player_dict1, maxim1):
    if player_dict1[0] + int(required1[0]) <= maxim1 and player_dict1[1] + int(required1[1]) <= maxim1 and player_dict1[
        2] + int(required1[2]) <= maxim1 and player_dict1[3] + int(required1[3]) <= maxim1 and player_dict1[4] + int(
        required1[4]) <= maxim1 and player_dict1[5] + int(required1[5]) <= maxim1 and player_dict1[6] + int(
        required1[6]) <= maxim1:
        return True
    return False


def get_occupied_dictionary(player_list2, player_eligible2):
    player_dic = {x: 0 for x in range(7)}
    for p in player_list2:
        days2 = player_eligible2.get(p)
        for days_index, days_val in enumerate(days2):
            player_dic[days_index] += int(days_val)
    return player_dic


def get_max_sum(input_array, dic, limit):
    max_sum_obj = MaxSum(input_array, dic, limit, {}, 0, [])
    max_sum_obj.collect_sums(0, 0)
    tup = (0, 0)
    if max_sum_obj.max != 0:
        tup = (max_sum_obj.max, max_sum_obj.sums[max_sum_obj.max])
    return tup


def get_max_score_by_player(input_arr, player_dic, max_limit, play):
    maxim_sum = get_max_sum(input_arr, player_dic, max_limit)[0]
    if play == "spla":
        return maxim_sum, 0
    else:
        return 0, maxim_sum


def get_eligible_apps(eligible1, player_list1, opponent_list1, maxim):
    response = []
    player_dict = get_occupied_dictionary(player_list1, eligible1)
    for app_key in eligible1.keys():
        if app_key not in player_list1 and app_key not in opponent_list1 and can_we_add_app_to_pool(eligible1[app_key], player_dict, maxim):
            response.append(app_key)
    return response


def terminal_node(p_eligible, p_list, o_eligible, o_list, p_max, o_max):
    opponent_qualified_list = get_eligible_apps(o_eligible, o_list, p_list, o_max)
    if not opponent_qualified_list or (len(opponent_qualified_list) == 1 and opponent_qualified_list[0] in p_eligible.keys()):
        lis = []
        for e in p_eligible.keys():
            if e not in p_list and e not in o_list:
                lis.append([e, p_eligible[e]])

        (max_sum, list_of_apps) = get_max_sum(lis, get_occupied_dictionary(p_list, p_eligible), p_max*7)
        if len(opponent_qualified_list) == 1 and opponent_qualified_list[0] in p_eligible.keys():
            pull_app = False
            if max_sum != 0:
                lowest_id = list_of_apps[0][0]
                for l in list_of_apps:
                    for a in l:
                        if int(a) < int(lowest_id):
                            lowest_id = a
                if opponent_qualified_list[0] == lowest_id:
                        pull_app = True
            if pull_app:
                return True, (opponent_qualified_list[0], max_sum)
            else:
                return False, ()
        if max_sum == 0:
            return True, ("0", max_sum)
        else:
            lowest_id = list_of_apps[0][0]
            for l in list_of_apps:
                for a in l:
                    if int(a) < int(lowest_id):
                        lowest_id = a
            return True, (lowest_id, max_sum)
    else:
        return False, ()


def get_next_node(level, player_eligible, opponent_eligible, player_list, opponent_list, player, opponent, player_max, opponent_max):
    (is_terminal, evaluation) = terminal_node(player_eligible, player_list, opponent_eligible, opponent_list, player_max, opponent_max)
    if is_terminal:
        (next_app, score) = evaluation
        final_dic = {next_app: (score, 0)}
        if player == "lahsa":
            final_dic = {next_app: (0, score)}
        return final_dic

    best_score = 0
    result = dict()
    eligible = get_eligible_apps(player_eligible, player_list, opponent_list, player_max)
    if level == 0:
        eligible.sort(key=int)
    for applicant in eligible:
        player_list.append(applicant)
        next_node = get_next_node(level + 1, opponent_eligible, player_eligible, opponent_list, player_list, opponent, player, opponent_max, player_max)
        if not next_node.keys():
            li = []
            for e in player_eligible.keys():
                if e not in player_list and e not in opponent_list:
                    li.append([e, player_eligible[e]])
            (tmp_spla, tmp_lahsa) = get_max_score_by_player(li, get_occupied_dictionary(player_list, player_eligible), player_max * 7, player)
        else:
            (tmp_spla, tmp_lahsa) = next_node[list(next_node.keys())[0]]
        (spla_score, lahsa_score) = (tmp_spla, tmp_lahsa)
        app_week_count = get_count_for_week(player_eligible[applicant])
        current_score = spla_score + app_week_count
        if player == "lahsa":
            current_score = lahsa_score + app_week_count
        if current_score >= best_score:
            if current_score == best_score:
                previous_id = list(result.keys())[0]
                if int(applicant) < int(previous_id):
                    result.clear()
                    result[applicant] = (current_score, lahsa_score)
                    if player == "lahsa":
                        result[applicant] = (spla_score, current_score)
                    if level == 0:
                        with open('output.txt', 'w') as output_file:
                            output_file.write(applicant)
            else:
                result.clear()
                result[applicant] = (current_score, lahsa_score)
                if player == "lahsa":
                    result[applicant] = (spla_score, current_score)
                if level == 0:
                    with open('output.txt', 'w') as output_file:
                        output_file.write(applicant)
            best_score = current_score
        player_list.remove(applicant)
    return result


if __name__ == "__main__":
    with open('input.txt', 'r') as inp:
        beds = int(inp.readline().strip())
        parking_spaces = int(inp.readline().strip())
        lahsa_count = int(inp.readline().strip())
        lahsa_arr = list()
        for i in range(lahsa_count):
            lahsa_arr.append(inp.readline().strip())
        spla_count = int(inp.readline().strip())
        spla_arr = list()
        for i in range(spla_count):
            spla_arr.append(inp.readline().strip())
        total = int(inp.readline().strip())
        spla_eligible = dict()
        lahsa_eligible = dict()
        for i in range(total):
            app = inp.readline().strip()
            app_id = app[:5]
            g = app[5:6]
            a = app[6:9]
            p = app[9:10]
            m = app[10:11]
            c = app[11:12]
            d = app[12:13]
            space = app[13:]
            if c == "Y" and d == "Y" and m == "N" and space != "0000000":
                spla_eligible[app_id] = space
            if g == "F" and int(a) > 17 and p == "N" and space != "0000000":
                lahsa_eligible[app_id] = space
        best_applicant = get_next_node(0, spla_eligible, lahsa_eligible, spla_arr, lahsa_arr, "spla", "lahsa", parking_spaces, beds)
        with open('output.txt', 'w') as output_file:
            output_file.write(list(best_applicant.keys())[0])