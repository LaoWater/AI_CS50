import csv
import sys
import time
from util_gamma import Node, StackFrontier, QueueFrontier, PriorityQueueFrontier

##########################################
#
##########################################

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

birth_years = {}


def get_birth_year(person_id):
    return birth_years.get(person_id)


def load_data(directory):
    """
    Load data from CSV files into memory and populate birth_years dictionary.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            person_id = row["id"]
            name = row["name"]
            birth = row["birth"] if row["birth"] != '' else None  # Handle missing birth years

            # Store person data
            people[person_id] = {
                "name": name,
                "birth": birth,
                "movies": set()
            }

            # Store birth year in birth_years dictionary
            birth_years[person_id] = int(birth) if birth is not None else None

            # Handle names (for potential duplicates)
            name_key = name.lower()
            if name_key not in names:
                names[name_key] = {person_id}
            else:
                names[name_key].add(person_id)
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


def heuristic(state, target):
    # Retrieve the birth years
    birth_year_state = get_birth_year(state)
    birth_year_target = get_birth_year(target)
    max_birth_year_difference = 40

    # Initialize heuristic cost
    h = 0

    # Birth Year Presence Penalty
    if birth_year_state is None:
        h += 2  # Penalty if birth year is missing

    # Birth Year Difference Penalty
    if birth_year_state is not None and birth_year_target is not None:
        birth_year_diff = abs(birth_year_state - birth_year_target)
        if birth_year_diff > 40:
            # Scale the penalty based on how far the difference is beyond 40
            h += (birth_year_diff - 40) / (max_birth_year_difference - 40)
    else:
        # If we can't compute the difference, assign a default penalty
        h += 1

    return h


def shortest_path(source, target):
    print(f"Starting A* search from {source} to {target}")
    explored_nodes = 0
    start_time = time.time()

    # Initialize the frontier using the starting node
    start = Node(state=source, parent=None, action=None, cost=0)
    frontier = PriorityQueueFrontier()
    frontier.add(start, priority=heuristic(start.state, target))

    # Initialize an empty explored set
    explored = set()

    while not frontier.empty():
        # Remove a node from the frontier
        node = frontier.remove()
        explored_nodes += 1

        # Print progress every 1111 explored nodes
        if explored_nodes % 1111 == 0:
            elapsed_time = time.time() - start_time
            print(f"\nExploring node #{explored_nodes}, elapsed time per 1111 nodes: {elapsed_time:.2f} seconds")
            start_time = time.time()

        # If the node contains the target state, return the solution
        if node.state == target:
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            print(f"Solution path: {path}")
            return path  # Returns a list of (movie_id, person_id) tuples

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to the frontier
        for action, state in neighbors_for_person(node.state):
            if state not in explored and not frontier.contains_state(state):
                child = Node(state=state, parent=node, action=action, cost=node.cost + 1)
                priority = child.cost + heuristic(child.state, target)
                frontier.add(child, priority)
            # Optionally, update the node in frontier if a better path is found
            # Implement this if necessary

    # If no path found
    print("No connection found.")
    return None


def construct_path(node_forward, node_backward):
    # Build path from source to meeting point
    path_forward = []
    while node_forward.parent is not None:
        path_forward.append((node_forward.action, node_forward.state))
        node_forward = node_forward.parent
    path_forward.reverse()

    # Build path from meeting point to target
    path_backward = []
    while node_backward.parent is not None:
        path_backward.append((node_backward.action, node_backward.state))
        node_backward = node_backward.parent

    return path_forward + path_backward


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
