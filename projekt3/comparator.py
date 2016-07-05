class Comparator:
    def make_ranking(self, parts_descriptions):
        array_of_comparisons = []
        array_of_comparisons2 = []
        for i in range(len(parts_descriptions)):
            pom2 = []
            pom3 = []
            for k in range(4):
                pom = []
                for j in range(len(parts_descriptions)):
                    if i == j:
                        continue

                    for n in range(4):
                        t1 = self.compare_2_edges(parts_descriptions[i][1][k], parts_descriptions[j][1][n])
                        t2 = self.compare_2_edges_inverted(parts_descriptions[i][1][k], parts_descriptions[j][1][n])
                        pom.append([min([t1, t2]), j])
                        pom3.append([min([t1, t2]), j])

                pom = sorted(pom)
                pom2.append(pom)
            array_of_comparisons.append(pom2)
            pom3 = sorted(pom3)
            array_of_comparisons2.append(pom3)
        return array_of_comparisons, array_of_comparisons2

    @staticmethod
    def compare_2_edges(edge1, edge2):
        inset1 = edge1[0]
        inset2 = edge2[0]

        if (inset1+inset2 == 0) and (inset1-inset2 != 0):
            points1 = edge1[1]
            points2 = edge2[1]

            sum_dif = 0.0
            for i in range(len(points1)):
                dif = 0.0

                dif += abs(points1[i][0] - points2[i][0])
                dif += abs(points1[i][1] - points2[i][1])
                dif += abs(points1[i][2] - points2[i][2])

                sum_dif += dif
            return sum_dif
        else:
            return 10000.0

    @staticmethod
    def compare_2_edges_inverted(edge1, edge2):
        pom = [edge2[0], list(reversed(edge2[1]))]
        return Comparator.compare_2_edges(edge1, pom)
