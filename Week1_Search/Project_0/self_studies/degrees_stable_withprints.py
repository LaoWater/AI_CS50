import csv
import sys
import time

from util import Node, StackFrontier, QueueFrontier

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
        sys.exit("Usage: python degrees_stable_withprints.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # print(f" People: {people}")  # Inspect the loaded people data
    # print(f" Movies: {movies}")  # Inspect the loaded movies data

    # source = person_id_for_name(input("Name: "))
    source = person_id_for_name("Jack Nicholson")
    if source is None:
        sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    target = person_id_for_name("Al Pacino")
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
    print(f"Starting search from {source} to {target}")
    explored_nodes = 0
    start_time = time.time()
    global_start_time = time.time()
    # Initialize the frontier using the starting node
    start = Node(state=source, parent=None, action=None)
    # DFS or BFS choice
    frontier = QueueFrontier()
    frontier.add(start)
    print(f"Initial frontier: {[node.state for node in frontier.frontier]}")

    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution is found
    while not frontier.empty():
        # Remove a node from the frontier
        node = frontier.remove()
        explored_nodes += 1
        # Print progress and elapsed time for every 1111 explored nodes
        if explored_nodes % 1111 == 0:
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            print(f"\nExploring node #{explored_nodes}, elapsed time per 1111 nodes: {elapsed_time:.2f} seconds")
            start_time = time.time()

        # If the node contains the target state, return the solution
        if node.state == target:
            print("Target found! Constructing path...")
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            global_compute_time = time.time() - global_start_time
            print(f"\nShortest Path compute time: {global_compute_time}")
            print(f"Solution path: {path}")
            return path  # Returns a list of (movie_id, person_id) tuples

        # Mark node as explored
        explored.add(node.state)
        # print(f"Marked {node.state} as explored.")

        # Add neighbors to the frontier
        neighbors = neighbors_for_person(node.state)
        # print(f"Neighbors found: {neighbors}")
        for action, state in neighbors:
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)
                # print(f"Added to frontier: {state} via action (movie) {action}")
            else:
                continue
                # print(f"Already in frontier or explored: {state}")

    global_compute_time = time.time() - global_start_time
    print(f"Shortest Path compute time: {global_compute_time}")
    # If no path found
    print("No connection found.")


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
            # print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
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
