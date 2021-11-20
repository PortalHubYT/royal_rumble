from time import sleep
import mc_api as mc

try:
    mc.connect("localhost", "test")
except ConnectionRefusedError:
    mc.create()
    mc.connect("localhost", "test")

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

def post(cmd, player="PortalHub"):
    return mc.post(f"sudo {player} /{cmd}")


mc.post("npc remove all")

# clean_up_npc(nb)
npc = ["Maria", "Paul", "Alex", "Tom"]
for name in npc:
    spawn_npc("Maria")
    print(ret)
    sleep(4)
