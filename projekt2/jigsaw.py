from statistics import mean


class Jigsaw:
    def __init__(self, edges_scores):
        self.edges_scores = edges_scores

    def solve(self, columns, rows):
        solution = []

        for i in range(columns):
            solution.append([])
            for j in range(rows):
                solution[i].append([])

        b_c, b_c_r = self.best_corner()
        solution[0][0] = [b_c, b_c_r]

        for i in range(columns):
            for j in range(rows):
                if (i == 0) and (j == 0):
                    continue
                if j == 0:
                    upper_element = solution[i-1][0]
                    upper_down_index = upper_element[1] % 4 + 1
                    current_element = self.edges_scores[upper_element[0]][upper_down_index][0][0][0]
                    current_upper_index = abs(self.edges_scores[upper_element[0]][upper_down_index][0][0][1])
                    current_right_index = current_upper_index % 4 + 1
                    solution[i][j] = [current_element, current_right_index]
                else:
                    left_element = solution[i][j-1]
                    left_right_index = left_element[1]
                    current_element = self.edges_scores[left_element[0]][left_right_index][0][0][0]
                    current_left_index = abs(self.edges_scores[left_element[0]][left_right_index][0][0][1])
                    current_upper_index = current_left_index % 4 + 1
                    current_right_index = current_upper_index % 4 + 1
                    solution[i][j] = [current_element, current_right_index]

        final_solution = []

        for i in range(columns):
            final_solution.append([])
            for j in range(rows):
                final_solution[i].append(solution[i][j][0])

        # calculate the value of solution
        value_of_solution = 0.0

        for i in range(columns-1):
            for j in range(rows):
                value_of_solution += self.edges_scores[solution[i][j][0]][solution[i][j][1]][0][1]
        for i in range(columns):
            for j in range(rows-1):
                current_down_index = solution[i][j][1] % 4 + 1
                value_of_solution += self.edges_scores[solution[i][j][0]][current_down_index][0][1]

        return final_solution, value_of_solution

    def best_corner(self):
        best_corner = 0
        best_diff = -1.0
        rotate = 0

        for i in range(len(self.edges_scores)):
            temp = []
            for j in range(1, 5):
                temp.append(self.edges_scores[i][j][0][1])
            temp = sorted(temp)

            # diff = temp[3] + temp[2] - temp[1] - temp[0]
            diff = mean([temp[3], temp[2]]) + temp[2] - mean([temp[1], temp[0]]) - temp[1]
            if best_diff < diff:
                best_diff = diff
                best_corner = i

                for j in range(1, 5):
                    if self.edges_scores[i][j][0][1] == temp[0]:
                        h = (j - 2) % 4 + 1
                        if self.edges_scores[i][h][0][1] == temp[1]:
                            rotate = h
                        else:
                            rotate = j

        # print(best_corner, rotate, best_diff)
        return best_corner, rotate
