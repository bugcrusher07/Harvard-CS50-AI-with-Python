import csv
import sys

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
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
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
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    if source == target:
        tempList = list(people[source]["movies"])
        list = [(tempList[0],source)]
        print("first Operation")
        return list

    queueObj =  QueueFrontier()
    sourceNode = Node(source,None,None)
    queueObj.add(sourceNode)
    for node in queueObj.frontier:
        print("node :  state- " + node.state )

    loopVar = True
    exploredNodes = []
    targetNode = None
    print("where are we")

    while ( loopVar ):
        if len(queueObj.frontier) == 0:
            loopVar = False
            print("breaking because of empty frontier")
            break
        else:
            tempExpNode = queueObj.remove()
            exploredNodes.append(tempExpNode)
            if tempExpNode.state == target:
                loopVar = False
                targetNode = tempExpNode
                print("not an exception break statement")
                break

            set = neighbors_for_person(tempExpNode.state)
            for movie_id,person_id in set:
                if if_person_id_not_in_frontier(person_id,queueObj.frontier) and person_id not in exploredNodes :
                    queueObj.add(Node(person_id,tempExpNode,movie_id))

    if targetNode!= None:
        print("target Node is not Null")
        return answer_list(targetNode,sourceNode)



def answer_list(targetNode,sourceNode):
    childNode = targetNode
    parentNode =sourceNode
    list = []
    loopVar = True
    while (loopVar):
        if childNode.parent != None:
            list.append((childNode.action,childNode.state))
            childNode = childNode.parent
        else:
            loopVar = False
            break
    return list

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

def if_person_id_not_in_frontier(person_id,frontier):
    list = []
    for node in frontier:
       list.append(node.state)
    if person_id in list:
        return False
    else:
        return True

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
