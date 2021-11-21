#!/usr/bin/python3

from io import DEFAULT_BUFFER_SIZE
from time import sleep
import time
from datetime import datetime

import mc_api as mc
import pytchat

try:
    mc.connect("localhost", "test")
except ConnectionRefusedError:
    mc.create()
    mc.connect("localhost", "test")

CHAT_ID = "4BCy5jYlSoo"
GAMEMASTER = "PortalHub"


def post(cmd, player=GAMEMASTER):
    return mc.post(f"sudo {player} /{cmd}")


def get_player_pos(player) -> mc.BlockCoordinates:
    coords = mc.post(f"data get entity {player}")

    coords = coords[coords.find("Pos") :]
    coords = coords[: coords.find("]")]
    coords = coords[coords.find("[") + 1 :]
    coords = coords.split(",")

    try:
        x = float(coords[0][:-1])
        y = float(coords[1][:-1])
        z = float(coords[2][:-1])
    except ValueError:
        x = 0.0
        y = 0.0
        z = 0.0

    return mc.BlockCoordinates(x, y, z)


def clean_npc():
    mc.post("npc remove all")


class Player:
    def __init__(self, name, pos):
        self.name = name
        self.x = pos.x
        self.y = pos.y
        self.z = pos.z + 15
        self.created_at = datetime.now()
        self.create_npc()

        self.path_to(mc.Coordinates(pos.x, pos.y, pos.z - 28))

    def create_npc(self):
        post(f"npc create {self.name} --at {self.x}:{self.y}:{self.z} --trait sentinel")
        post("sentinel speed 1")
        post("waypoints disableteleport")
        post("npc pathfindingrange 300")
        post("sentinel respawntime -1")
        post("npc pathopt --use-new-finder true")

    def path_to(self, pos):
        post(f"npc pathto {pos.x} {pos.y} {pos.z}")
        sleep(0.5)
        post(f"npc pathto {pos.x} {pos.y} {pos.z}")

    def make_agro(self):
        post(f"npc sel {self.name}")
        post("sentinel addtarget npcs")


queue = []

clean_npc()
names = [f"bot-{str(x)}" for x in range(150)]

i = 0


def name_list():
    i = 0
    while i < len(names):
        yield names[i]
        i += 1


spawn_pos = mc.Coordinates(-148.5, 19, 135.5)
name = name_list()
while True:

    queue.append(Player(next(name), spawn_pos))

    for p in queue:

        if (datetime.now() - p.created_at).total_seconds() > 20:
            queue.remove(p)
            p.make_agro()
    sleep(1)


# while True:
#     chat = pytchat.create(video_id=CHAT_ID)
#     for c in chat.get().sync_items():
#         msg = c.message
#         print(msg)
#         if msg.startswith("/enter "):
#             pseudo = msg.split(" ")[1]
#             create_npc(pseudo, -150, 20, 20)
#     sleep(0.1)
