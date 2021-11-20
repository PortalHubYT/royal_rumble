from io import DEFAULT_BUFFER_SIZE
from time import sleep
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


def create_npc(name):
    post(f"npc create {name} --trait sentinel")
    post("sentinel respawntime -1")
    post("sentinel addtarget npcs")


while True:
    chat = pytchat.create(video_id=CHAT_ID)
    for c in chat.get().sync_items():
        msg = c.message
        print(msg)
        if msg.startswith("/enter "):
            pseudo = msg.split(" ")[1]
            create_npc(pseudo)
    sleep(0.1)
