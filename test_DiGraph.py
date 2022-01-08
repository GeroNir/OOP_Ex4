from unittest import TestCase
from DiGraph import DiGraph


class TestDiGraph(TestCase):

    def test_v_size(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual(11, g.v_size())

    def test_e_size(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual(22, g.e_size())
        g.add_edge(0, 3, 5.367)
        self.assertEqual(23, g.e_size())
        g.add_edge(0, 1, 1.32131)
        self.assertEqual(1, g.get_mc())
        self.assertFalse(g.add_edge(15, 0, 3.61786378))

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        ans = g.all_in_edges_of_node(0)
        a1 = ans.get(0)[0]['dest']
        a2 = ans.get(0)[1]['dest']
        self.assertEqual(0, a1)
        self.assertEqual(0, a2)

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        ans = g.all_out_edges_of_node(0)
        a1 = ans.get(0)[0]['src']
        a2 = ans.get(0)[1]['src']
        self.assertEqual(0, a1)
        self.assertEqual(0, a2)

    def test_get_mc(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        g.remove_node(0)
        self.assertEqual(5, g.get_mc())
        g.add_node(0)
        self.assertEqual(6, g.get_mc())
        g.remove_edge(5, 4)
        self.assertEqual(7, g.get_mc())
        g.remove_edge(0, 1)
        self.assertEqual(7, g.get_mc())

    def test_add_edge(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        g.add_edge(0, 3, 1.463275)
        key = "0,3"
        self.assertEqual(g.Edges[key]['w'], 1.463275)

    def test_add_node(self):
        g = DiGraph()
        g.add_node(0, (1, 2, 3))
        g.add_node(1, (4, 2, 3))
        g.add_node(2, (1, 6, 3))
        g.add_node(3)
        self.assertEqual(4, g.v_size())
        self.assertEqual(g.get_pos(0), (1,2,3))

    def test_remove_node(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertTrue(g.remove_node(0))
        self.assertFalse(g.remove_node(0))
        self.assertEqual(5, g.get_mc()) # 5 because it have 4 edges that goes in/out

    def test_remove_edge(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertTrue(g.remove_edge(0,1))
        self.assertFalse(g.remove_edge(0,1))
        self.assertEqual(1, g.get_mc())  # 5 because it have 4 edges that goes in/out

    def test_get_node(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual("{'pos': '35.19341035835351,32.10610841680672,0.0', 'id': 2}", str(g.get_node(2)))

    def test_get_pos(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual("35.19341035835351,32.10610841680672,0.0", str(g.get_pos(2)))

    def test_get_x(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual("35.19341035835351", str(g.get_x(2)))

    def test_get_y(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual("32.10610841680672", str(g.get_y(2)))

    def test_get_z(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual("0.0", str(g.get_z(2)))