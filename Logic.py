import math as ma
import queue
from types import SimpleNamespace
from DiGraph import DiGraph
import json
import pygame
import GraphAlgo

def dist(p1, p2):
    delta = ma.sqrt(ma.pow(float(p1.x - p2.x), 2) + ma.pow(float(p1.y - p2.y), 2))
    return delta


def findEdge(graph, Edges, pos):
    x, y, z = str(pos).split(',')
    pos = SimpleNamespace(x=float(x), y=float(y))
    min = 10000000000
    for e in Edges:
        # print(graph['Nodes'][e['dest']]['pos'])
        delta1 = dist(graph['Nodes'][e['src']]['pos'], graph['Nodes'][e['dest']]['pos'])
        delta2 = dist(graph['Nodes'][e['src']]['pos'], pos) + dist(pos, graph['Nodes'][e['dest']]['pos'])
        delta = ma.fabs(delta1 - delta2)
        if delta < min:
            min = delta
            edge = e
    return edge

def start(client, graph):

    clock = pygame.time.Clock()

    g = DiGraph()
    path = client.get_info().split(",")

    path = path[7][9:-1]
    algo = GraphAlgo.GraphAlgo(g)
    algo.load_from_json(path)

    info = client.get_info().split(',')
    grade = info[3]
    grade = grade[8:]

    num_of_agentes = info[8]
    num_of_agentes = num_of_agentes[9:-2]
    num_of_agentes = int(num_of_agentes)
    allocate = []

    for i in range(num_of_agentes):
        q = queue.Queue()
        allocate.append(q)

    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]

    pokemons = json.loads(client.get_pokemons())
    pokemons = [p["Pokemon"] for p in pokemons["Pokemons"]]

    allocate = []

    for i in range(num_of_agentes):
        q = queue.Queue()
        allocate.append(q)

    list_edegs = []

    for p in pokemons:
        e = findEdge(graph, graph['Edges'], p['pos'])
        if p['type'] == 1:
            list_edegs.append(e['dest'])
        else:
            list_edegs.append(e['src'])
    # choose next edge
    if len(agents) == 1:
        for agent in agents:
            # find where the agent
            for n in graph['Nodes']:
                x, y, z = str(agent.pos).split(',')
                if float(n['pos'].x) == float(x) and float(n['pos'].y) == float(y):
                    node = n['id']
            if agent.dest == -1:
                for p in pokemons:
                    e = findEdge(graph, graph['Edges'], p['pos'])
                    if not node == e['src']:
                        dest = algo.shortest_path(node, e['src'])[1]
                    else:
                        dest = algo.shortest_path(node, e['dest'])[1]
                for i in dest:
                    allocate[agent.id].put_nowait(i)

                for i in range(allocate[agent.id].qsize()):
                    client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(
                        allocate[agent.id].get()) + '}')
                    pygame.time.wait(2)

                ttl = client.time_to_end()
                print(ttl, client.get_info())

        clock.tick(11)
        client.move()
        pygame.time.wait(20)

    else:
        for p in pokemons:
            count = 0
            e = findEdge(graph, graph['Edges'], p['pos'])
            min = 10000000
            index = -1
            for agent in agents:
                count += 1
                if agent.dest == -1:
                    # find where the agent
                    for n in graph['Nodes']:
                        x, y, z = str(agent.pos).split(',')
                        if float(n['pos'].x) == float(x) and float(n['pos'].y) == float(y):
                            node = n['id']
                    if p['type'] == 1 and node != e['dest']:
                        delta, dest = algo.shortest_path(node, e['dest'])
                    else:
                        delta, dest = algo.shortest_path(node, e['src'])
                    if delta < min:
                        min = delta
                        index = agent.id
                    if count == num_of_agentes:
                        allocate[index].put_nowait(e['src'])
                        for i in dest:
                            allocate[index].put_nowait(i)
                        allocate[index].put_nowait(e['dest'])
                        pygame.time.wait(1)
                        client.choose_next_edge(
                            '{"agent_id":' + str(index) + ', "next_node_id":' + str(allocate[index].get()) + '}')
                        #tmp = allocate[index].get()
                        #if node != tmp:
                            #allocate[index].put(tmp)
                    for i in range(allocate[agent.id].qsize()):
                        client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(
                            allocate[agent.id].get(timeout=1000)) + '}')
                        pygame.time.wait(1)

        ttl = client.time_to_end()
        print(ttl, client.get_info())
        if int(grade) > 150:
            clock.tick(12)
        else:
            clock.tick(10)
        client.move()