from io import DEFAULT_BUFFER_SIZE
from time import sleep
import mc_api as mc

try:
    mc.connect("localhost", "test")
except ConnectionRefusedError:
    mc.create()
    mc.connect("localhost", "test")


def post(cmd, player="PortalHub"):
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


mc.post("npc remove all")

# clean_up_npc(nb)
npc = ["Maria", "Paul", "Alex", "Tom"]
for name in npc:
    ret = post(f"npc create {name} --trait sentinel")
    print(ret)
    ret = post("sentinel respawntime -1")
    print(ret)
    ret = post("sentinel addtarget npcs")
    print(ret)
    sleep(4)
