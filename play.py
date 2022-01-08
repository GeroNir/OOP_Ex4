import json
from client import Client


class Play:

    def __init__(self):
        self.client = Client()

    def get_score(self):
        json_grade = json.loads(self.client.get_info())
        return json_grade['GameServer']['grade']

    def get_graph_file_name(self):
        json_graph_file = json.loads(self.client.get_info())
        return "../" + json_graph_file['GameServer']['graph']

    def get_moves(self):
        json_moves = json.loads(self.client.get_info())
        return json_moves['GameServer']['moves']

    def time_remaining(self):
        return self.client.time_to_end()