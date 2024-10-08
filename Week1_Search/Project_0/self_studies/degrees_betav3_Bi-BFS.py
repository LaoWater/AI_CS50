import csv
import sys
import time
from types import NoneType
from util import Node, StackFrontier, QueueFrontier


# V3 - addressing the shortest path
# Tracking Levels:
# forward_level and backward_level are used to track how many levels each search has expanded.
# Controlled Expansion:
# We only expand the backward frontier if the backward_level is strictly less than forward_level, ensuring that the forward search stays ahead.
# Bias Toward Forward Search:
# The forward search is always allowed to expand if it's at the same level as the backward search, ensuring that it is always "ahead."
# How It Works:
# The forward search will always stay at least one level ahead of the backward search.
# If both are at the same level, the forward search is expanded first, making sure the first meeting point is the shortest path.
# This ensures that the backward search doesn't over-expand, and the shortest path is guaranteed.

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # source = person_id_for_name(input("Name: "))
    source = person_id_for_name("Minnie Driver")
    if source is None:
        sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    target = person_id_for_name("Jennifer Ehle")
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    print(f"Starting bidirectional search from {source} to {target}")
    explored_nodes = 0
    start_time = time.time()
    global_start_time = time.time()

    # Initialize the frontiers and explored sets
    frontier_forward = QueueFrontier()
    frontier_backward = QueueFrontier()
    frontier_forward.add(Node(state=source, parent=None, action=None))
    frontier_backward.add(Node(state=target, parent=None, action=None))

    explored_forward = {}
    explored_backward = {}

    # Track the levels of forward and backward searches
    forward_level = 0
    backward_level = 0

    # Keep looping until both frontiers are empty or solution is found
    while not frontier_forward.empty() and not frontier_backward.empty():

        # Expand forward frontier if forward_level <= backward_level
        if forward_level <= backward_level:
            node_forward = frontier_forward.remove()
            # print(f"Exploring forward node {node_forward.state}")
            explored_nodes += 1
            explored_forward[node_forward.state] = node_forward

            # Explore neighbors in the forward direction
            neighbors_forward = neighbors_for_person(node_forward.state)
            # print(f"Neighbors of forward node {node_forward.state}: {neighbors_forward}")
            for action, state in neighbors_forward:
                if state not in explored_forward and not frontier_forward.contains_state(state):
                    # print(f"Adding to forward frontier: forward neighbor {state} via action {action}")
                    child_forward = Node(state=state, parent=node_forward, action=action)
                    if state in explored_backward:
                        print(f"Forward path meets backward path at {state}")
                        global_compute_time = time.time() - global_start_time
                        print(f"\nShortest Path compute time: {global_compute_time}")
                        print(f"Explored Nodes: {explored_nodes}")
                        return construct_bidirectional_path(child_forward, explored_backward[state])

                    frontier_forward.add(child_forward)
            forward_level += 1  # Increase forward level after expansion

        # Expand backward frontier only if backward_level < forward_level
        if backward_level < forward_level - 1:
            node_backward = frontier_backward.remove()
            # print(f"Exploring backward node {node_backward.state}")
            explored_nodes += 1
            explored_backward[node_backward.state] = node_backward

            # Explore neighbors in the backward direction
            neighbors_backward = neighbors_for_person(node_backward.state)
            # print(f"Neighbors of backward node {node_backward.state}: {neighbors_backward}")
            for action, state in neighbors_backward:
                if state not in explored_backward and not frontier_backward.contains_state(state):
                    # print(f"Adding to backward frontier: backward neighbor {state} via action {action}")
                    child_backward = Node(state=state, parent=node_backward, action=action)
                    if state in explored_forward:
                        print(f"Backward path meets forward path at {state}")
                        global_compute_time = time.time() - global_start_time
                        print(f"\nShortest Path compute time: {global_compute_time}")
                        print(f"Explored Nodes: {explored_nodes}")
                        return construct_bidirectional_path(explored_forward[state], child_backward)

                    frontier_backward.add(child_backward)
            backward_level += 1  # Increase backward level after expansion

        # Print progress for every 1111 nodes explored
        if explored_nodes % 1111 == 0:
            elapsed_time = time.time() - start_time
            print(f"\nExploring node #{explored_nodes}, elapsed time per 1111 nodes: {elapsed_time:.2f} seconds")
            start_time = time.time()

    print("No connection found.")
    return None



def construct_bidirectional_path(forward_node, backward_node):
    """
    Constructs the full path from the source to the target by combining
    the forward and backward paths at the meeting point.
    """
    last_forward_node_action = None
    # 1. Parse forward nodes
    path_forward = []
    print("\n--- Parsing Forward Nodes ---")
    while forward_node.parent is not None:
        print(f"Forward node {forward_node.state}, action {forward_node.action}")
        path_forward.append((forward_node.action, forward_node.state))
        last_forward_node_action = forward_node.action
        forward_node = forward_node.parent

    # Don't forget to add the root node (source)
    # path_forward.append((None, forward_node.state))  # No action for source
    path_forward.reverse()  # Reverse to go from source to meeting point
    print(path_forward)

    # 2. Parse backward nodes (carefully skipping the meeting point)
    path_backward = []
    last_backward_node_action = None
    print("\n--- Parsing Backward Nodes ---")
    while backward_node.parent is not None:
        # Skip the first backward node if it's already in the forward path (meeting point)
        if len(path_forward) > 0:
            if backward_node.state == path_forward[-1][1]:
                print(f"Skipping meeting point {backward_node.state} in backward path.")
                backward_node = backward_node.parent
                continue

        print(f"Backward node {backward_node.state}, action {backward_node.action}")
        path_backward.append((backward_node.action, backward_node.state))
        last_backward_node_action = backward_node.action
        backward_node = backward_node.parent

    # 3. Handle target node (which has no parent and no action)
    # For scenarios in which backward path is: many nodes, 1 node, no nodes.
    if len(path_backward) > 1:
        path_backward.append((last_backward_node_action, backward_node.state))  # No action for target
    else:
        path_backward.append((last_forward_node_action, backward_node.state))

    # 4. Combine forward and backward paths
    full_path = path_forward + path_backward
    print(f"\nFull path: {full_path}")

    return full_path



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
