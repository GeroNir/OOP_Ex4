from unittest import TestCase

from GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):

    def test_load_from_json(self):
        algo = GraphAlgo()
        algo.load_from_json('data/A0.json')
        n = algo.get_graph().Nodes[0]
        tmp = "{'pos': '35.18753053591606,32.10378225882353,0.0', 'id': 0}"
        self.assertEqual(str(n), tmp)

    def test_shortest_path(self):
        algo = GraphAlgo()
        algo.load_from_json('data/A0.json')
        ans = "(7.5417591783049245, [1, 0, 10, 9, 8, 7])"
        self.assertEqual(ans, str(algo.shortest_path(1, 7)))

    def test_tsp(self):
        algo = GraphAlgo()
        algo.load_from_json('data/A0.json')
        list = [2, 5, 6, 1, 3]
        ans = [3, 2, 1, 5, 6]
        self.assertEqual(ans, algo.TSP(list))

    def test_save_to_json(self):
        algo = GraphAlgo()
        algo.load_from_json('data/A0.json')
        first = algo.get_graph().get_all_v()
        print(first)
        algo.save_to_json('data/test.json')
        algo.load_from_json('data/test.json')
        second = algo.get_graph().get_all_v()
        print(second)
        self.assertEqual(str(first), str(second))

    def test_center_point(self):
        algo = GraphAlgo()
        algo.load_from_json('data/A0.json')
        ans = (1, 6.806805834715163)
        self.assertEqual(ans, algo.centerPoint())
