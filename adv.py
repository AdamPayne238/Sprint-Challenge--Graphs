from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
print("THIS", player.current_room.id)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

backwards_path = []

# Add backwards directions to get out of rooms with no exits by going back to previous rooms
backwards_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# Create visited dictionary
visited = {}

# Start in room 0 with current exits
visited[0] = player.current_room.get_exits()

# Loop while we have not visited all rooms in room_graph
while len(visited) < len(room_graph):
    # Check if current room not in visited
    if player.current_room.id not in visited:
        visited[player.current_room.id] = player.current_room.get_exits()
        last_path = backwards_path[-1]
        visited[player.current_room.id].remove(last_path)
    # Loop backwards once we reach a room with no directions
    while len(visited[player.current_room.id]) < 1:
        # Pop the back to last set of get exits and append it to traversal path
        backwards = backwards_path.pop()
        traversal_path.append(backwards)
        # Now we travel backwards
        player.travel(backwards)
    # Pop current room from visited
    exit_room = visited[player.current_room.id].pop(0)
    # Append it to traversal path
    traversal_path.append(exit_room)
    backwards_path.append(backwards_directions[exit_room])
    player.travel(exit_room)

    print(len(room_graph) - len(visited))
    if len(room_graph) - len(visited) == 1:
        visited[player.current_room.id] = player.current_room.get_exits()




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
"""
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
"""
