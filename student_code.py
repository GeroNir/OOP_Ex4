"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import math as ma
import queue
from types import SimpleNamespace
from queue import *

import Pokemons
from DiGraph import DiGraph
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
import GraphAlgo

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(graph_json)

# print("graph", graph['Nodes'])

for n in graph['Nodes']:
    x, y, _ = str(n['pos']).split(',')
    n['pos'] = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph['Nodes']), key=lambda n: n['pos'].x)['pos'].x
min_y = min(list(graph['Nodes']), key=lambda n: n['pos'].y)['pos'].y
max_x = max(list(graph['Nodes']), key=lambda n: n['pos'].x)['pos'].x
max_y = max(list(graph['Nodes']), key=lambda n: n['pos'].y)['pos'].y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


def dist(p1, p2):
    delta = ma.sqrt(ma.pow(float(p1.x - p2.x), 2) + ma.pow(float(p1.y - p2.y), 2))
    return delta


def findEdge(Edges, pos):
    x, y, z = str(pos).split(',')
    pos = SimpleNamespace(x=float(x), y=float(y))
    min = 10000000000
    for e in Edges:
        #print(graph['Nodes'][e['dest']]['pos'])
        delta1 = dist(graph['Nodes'][e['src']]['pos'], graph['Nodes'][e['dest']]['pos'])
        delta2 = dist(graph['Nodes'][e['src']]['pos'], pos) + dist(pos, graph['Nodes'][e['dest']]['pos'])
        delta = ma.fabs(delta1 - delta2)
        if delta < min:
            min = delta
            edge = e
    return edge


radius = 15

client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()
q = queue.Queue()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons())
    pokemons = [p["Pokemon"] for p in pokemons["Pokemons"]]
    for p in pokemons:
        # print("P", p['pos'])
        x, y, _ = p["pos"].split(',')
        # print(x)
        # print(y)
        p["pos"] = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    # print(agents)
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph['Nodes']:
        x = my_scale(n['pos'].x, x=True)
        y = my_scale(n['pos'].y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n['id']), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph['Edges']:
        # find the edge nodes
        src = next(n for n in graph['Nodes'] if n['id'] == e['src'])
        dest = next(n for n in graph['Nodes'] if n['id'] == e['dest'])

        # scaled positions
        src_x = my_scale(src['pos'].x, x=True)
        src_y = my_scale(src['pos'].y, y=True)
        dest_x = my_scale(dest['pos'].x, x=True)
        dest_y = my_scale(dest['pos'].y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        tmp = Pokemons.Pokemon(p)
        pygame.draw.circle(screen, Color(0, 255, 255), (int(tmp.x), int(tmp.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    g = DiGraph()
    path = client.get_info().split(",")

    path = path[7][9:-1]
    #print(path)
    algo = GraphAlgo.GraphAlgo(g)
    algo.load_from_json(path)
    last_agent = 0

    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    # choose next edge
    # if q.empty():
    for agent in agents:
        if agent.dest == -1:
            last_agent = agent.id
            pokemons = json.loads(client.get_pokemons())
            pokemons = [p["Pokemon"] for p in pokemons["Pokemons"]]
            for p in pokemons:
                print(p)
                e = findEdge(graph['Edges'], p['pos'])
                next_node = e['src']
                for n in graph['Nodes']:
                    x,y,z = str(agent.pos).split(',')
                    if float(n['pos'].x) == float(x) and float(n['pos'].y) == float(y):
                        node = n['id']
                #print("node", node)
                print(node, e['src'])
                if len(pokemons) > 1:
                    dest_node = algo.TSP()
                if not node == e['src']:
                    dest = algo.shortest_path(node, e['src'])[1]
                else:
                    dest = algo.shortest_path(node, e['dest'])[1]
                print(dest[1])
                dest = dest[1]
                client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(dest) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
    clock.tick(10)
    client.move()
# game over: