# class Agent:
#     def __init__(self, info: dict):
#         self.id = int(info['id'])
#         self.value = float(info['value'])
#         self.src = int(info['src'])
#         self.dest = int(info['dest'])
#         self.nextPok = []
#         self.nextNode = []
#         self.speed = float(info['speed'])
#         pos = str(info['pos'])
#         loc = pos.split(',')
#         self.x = float(loc[0])
#         self.y = float(loc[1])
#
#
#  for p in pokemons:
#             count = 0
#             dest = 0
#             e = findEdge(graph['Edges'], p['pos'])
#             # last_agent = agent.id
#             delta = 0
#             min = 10000000
#             index = -1
#             for agent in agents:
#                 count += 1
#                 print("gets into agents")
#                     for n in graph['Nodes']:
#                         print("gets into graph['Nodes']")
#                         x, y, z = str(agent.pos).split(',')
#                         if float(n['pos'].x) == float(x) and float(n['pos'].y) == float(y):
#                             node = n['id']
#                     print(e['dest'], e['src'], node)
#                     if p['type'] == 1 and node != e['dest']:
#                         delta, dest = algo.shortest_path(node, e['dest'])
#                         print("1", dest)
#                     else:
#                         delta, dest = algo.shortest_path(node, e['src'])
#                         print("-1", dest)
#                     if delta < min && count == num_of_agentes:
#                         min = delta
#                         index = agent.id
#                         agent.nextPok.append(index)
#                         # client.choose_next_edge('{"agent_id":' + str(index) + ', "next_node_id":' + str(dest[1]) + '}')
#             ttl = client.time_to_end()
#             print(ttl, client.get_info())
#         clock.tick(11)
#         client.move()
