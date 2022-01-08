import queue
from types import SimpleNamespace
import Logic
import Pokemons
from DiGraph import DiGraph
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
import pygame_widgets
from pygame_widgets.button import Button
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

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(graph_json)

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

g = DiGraph()
path = client.get_info().split(",")

path = path[7][9:-1]
algo = GraphAlgo.GraphAlgo(g)
algo.load_from_json(path)
last_agent = 0
cen = algo.centerPoint()

info = client.get_info().split(',')
num_of_agents = info[8]
num_of_agents = num_of_agents[9:-2]
num_of_agents = int(num_of_agents)
allocate = []

for i in range(num_of_agents):
    q = queue.Queue()
    tmp = "{\"id\":" + str(cen[0]) + "}"
    client.add_agent(tmp)
    allocate.append(q)
radius = 15

button = Button(
    screen, 20, 650, 100, 50, text='Exit',
    fontSize=50, margin=20,
    pressedColour=(0, 255, 0), radius=20,
    onClick=lambda: exit(0)
)

# this command starts the server - the game is running now
client.start()


while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons())
    pokemons = [p["Pokemon"] for p in pokemons["Pokemons"]]
    for p in pokemons:
        x, y, _ = p["pos"].split(',')
        p["pos"] = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]

    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    bg = pygame.image.load("graphics/canyon.jpg")
    # INSIDE OF THE GAME LOOP
    screen.blit(bg, (0, 0))

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
        ash = pygame.image.load("graphics/ash.png")
        screen.blit(ash, ((int(agent.pos.x), int(agent.pos.y))))

    x = (WIDTH * 0.45)
    y = (HEIGHT * 0.8)
    pok = pygame.image.load("graphics/pikachu.png")
    for p in pokemons:
        tmp = Pokemons.Pokemon(p)
        screen.blit(pok, ((int(tmp.x), int(tmp.y))))

    # update screen changes
    display.update()

    # prints results:
    json_grade = json.loads(client.get_info())
    font = pygame.font.SysFont('Comic Sans MS', 30)
    score = "SCORE: " + str(json_grade['GameServer']['grade'])
    print("score", score)
    text1 = font.render(score, False, (0, 0, 255))
    screen.blit(text1, (220, 20))

    moves = "MOVES: " + str(json_grade['GameServer']['moves'])
    print("moves", moves)
    text2 = font.render(moves, False, (0, 255, 0))
    screen.blit(text2, (400, 20))

    timeleft = float(client.time_to_end()) / 1000
    timeleft = "TIME LEFT: " + str(timeleft)
    print("time left", timeleft)
    text3 = font.render(timeleft, False, (0, 0, 0))
    screen.blit(text3, (20, 120))

    events = pygame.event.get()
    if event.type == pygame.QUIT:
        pygame.quit()
        run = False
        quit()

    pygame_widgets.update(events)
    pygame.display.update()

    Logic.start(client, graph)
