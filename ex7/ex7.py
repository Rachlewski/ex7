import csv

# Global BST root
OWNER_ROOT = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")
HONEN_DATA_BY_NAME = {}

def map_honen_data_by_name():
    for poke in HOENN_DATA:
        HONEN_DATA_BY_NAME[poke["Name"]] = poke

map_honen_data_by_name()

owner_root = None

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            pass

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    if poke_id > len(HOENN_DATA):
        return None
    return HOENN_DATA[poke_id - 1]

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    for poke in HOENN_DATA:
        if poke["Name"] == name:
            return poke
    return None

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    if len(poke_list) == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return
    for poke in poke_list:
        print(f"ID: {poke['ID']}, Name: {poke['Name']}, Type: {poke['Type']}, HP: {poke['HP']}, Attack: {poke['Attack']}, Can Evolve: {poke['Can Evolve']}")

########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    owner_node = {
        "owner": owner_name,
        "pokedex": [first_pokemon],
        "left": None,
        "right": None
    }
    return owner_node

def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    if root is None:
        print(f"New Pokedex created for {new_node['owner']} with starter {new_node['pokedex'][0]['Name']}.")
        return new_node
    if new_node["owner"].lower() < root["owner"].lower():
        root["left"] = insert_owner_bst(root["left"], new_node)
    elif new_node["owner"].lower() > root["owner"].lower():
        root["right"] = insert_owner_bst(root["right"], new_node)
    else:
        print(f"Owner '{new_node['owner']}' already exists. No new Pokedex created.")
    return root

def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    if root is None:
        return None
    if root["owner"].lower() == owner_name.lower():
        return root
    elif root["owner"].lower() > owner_name.lower():
        return find_owner_bst(root["left"], owner_name)
    else:
        return find_owner_bst(root["right"], owner_name)

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    if node["left"] is None:
        return node
    return min_node(node["left"])

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    if root is None:
        return None
    
    # First locate the node to delete
    if root["owner"].lower() > owner_name.lower():
        root["left"] = delete_owner_bst(root["left"], owner_name)
    elif root["owner"].lower() < owner_name.lower():
        root["right"] = delete_owner_bst(root["right"], owner_name)
    else:
        # No children
        if root["left"] is None and root["right"] is None:
            return None
            
        #  One child
        if root["left"] is None:
            return root["right"]
        elif root["right"] is None:
            return root["left"]
        
        # Two children
        successor = min_node(root["right"])
        root["owner"] = successor["owner"]
        root["pokedex"] = successor["pokedex"]
        root["right"] = delete_owner_bst(root["right"], successor["owner"])
    
    return root


########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    if root is None:
        return
    queue = [root]
    while queue:
        node = queue.pop(0)
        print(f"Owner: {node['owner']}")
        display_pokemon_list(node["pokedex"])
        print("")
        if node["left"] is not None:
            queue.append(node["left"])
        if node["right"] is not None:
            queue.append(node["right"])

# def pre_order(root):
#     """
#     Pre-order traversal (root -> left -> right). Print data for each node.
#     """
    

# def in_order(root):
#     """
#     In-order traversal (left -> root -> right). Print data for each node.
#     """
#     pass

# def post_order(root):
#     """
#     Post-order traversal (left -> right -> root). Print data for each node.
#     """
#     pass


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    pokemon_id = read_int_safe("Enter Pokemon ID to add:")
    pokemon_data = get_poke_dict_by_id(pokemon_id)
    if pokemon_data is None:
        print(f"Pokemon with ID {pokemon_id} not found.")
        return
    if insert_pokemon(owner_node, pokemon_data):
        print(f"Pokemon {pokemon_data['Name']} (ID {pokemon_data['ID']}) added to {owner_node['owner']}'s pokedex.")
    else:
        print(f"Pokemon already in the list. No changes made.")

def insert_pokemon(owner_node, pokemon_data):
    if pokemon_data in owner_node["pokedex"]:
        return False
    owner_node["pokedex"].append(pokemon_data)
    return True

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    to_release = input("Enter Pokemon Name to release:")
    if remove_pokemon_by_name(owner_node, to_release):
        print(f"Releasing {to_release} from {owner_node['owner']}.")
    else:
        print(f"No Pokemon named '{to_release}' in {owner_node['owner']}'s pokedex.")

def remove_pokemon_by_name(owner_node, poke_name):
    for poke in owner_node["pokedex"]:
        if poke["Name"] == poke_name:
            owner_node["pokedex"].remove(poke)
            return True
    return False

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    to_evolve = input("Enter Pokemon Name to evolve:")
    pokemon_data = get_poke_dict_by_name(to_evolve)
    if len([poke for poke in owner_node["pokedex"] if poke["Name"] == to_evolve]) == 0:
        print(f"No Pokemon named '{to_evolve}' in {owner_node['owner']}'s pokedex.")
        return
    if pokemon_data["Can Evolve"] == "FALSE":
        print(f"Pokemon {to_evolve} cannot evolve.")
        return
    evolved_pokemon = get_poke_dict_by_id(pokemon_data["ID"] + 1)
    print(f"Pokemnon evolved from {pokemon_data['Name']} (ID {pokemon_data['ID']}) to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
    remove_pokemon_by_name(owner_node, to_evolve)
    for poke in owner_node["pokedex"]:
        if poke["Name"] == evolved_pokemon["Name"]:
            print(f"{evolved_pokemon['Name']} was already present; releasing it immediately.")
            return
    insert_pokemon(owner_node, evolved_pokemon)



########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    if root is None:
        return
    gather_all_owners(root["left"], arr)
    arr.append(root)
    gather_all_owners(root["right"], arr)

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    global OWNER_ROOT
    if OWNER_ROOT is None:
        print("No owners at all.")
        return
    owners = []
    gather_all_owners(OWNER_ROOT, owners)
    print("=== The Owners we have, sorted by number of Pokemons ===")
    
    n = len(owners)
    for i in range(n):
        for j in range(0, n - i - 1):
            size1 = len(owners[j]['pokedex'])
            size2 = len(owners[j + 1]['pokedex'])
            if size1 > size2 or (size1 == size2 and owners[j]['owner'] > owners[j + 1]['owner']):
                owners[j], owners[j + 1] = owners[j + 1], owners[j]
    for owner in owners:
        print(f"Owner:{owner['owner']} (has {len(owner['pokedex'])} Pokemon)")


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    global OWNER_ROOT
    print("1) BFS")
    print("2) Pre-Order")
    print("3) In-Order")
    print("4) Post-Order")
    choice = read_int_safe("Your choice:")
    if choice == 1:
        bfs_traversal(OWNER_ROOT)
    elif choice == 2:
        pre_order_print(OWNER_ROOT)
    elif choice == 3:
        in_order_print(OWNER_ROOT)
    elif choice == 4:
        post_order_print(OWNER_ROOT)

def pre_order_print(node):
    """
    Helper to print data in pre-order.
    """
    if node is None:
        return
    print(f"Owner: {node['owner']}")
    display_pokemon_list(node["pokedex"])
    print("")
    pre_order_print(node["left"])
    pre_order_print(node["right"])

def in_order_print(node):
    """
    Helper to print data in in-order.
    """
    if node is None:
        return
    in_order_print(node["left"])
    print(f"Owner: {node['owner']}")
    display_pokemon_list(node["pokedex"])
    print("")
    in_order_print(node["right"])

def post_order_print(node):
    """
    Helper to print data in post-order.
    """
    if node is None:
        return
    post_order_print(node["left"])
    post_order_print(node["right"])
    print(f"Owner: {node['owner']}")
    display_pokemon_list(node["pokedex"])
    print("")


########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    while True:
        print("-- Display Filter Menu --")
        print("1. Only a certain type")
        print("2. Only Evolvable")
        print("3. Only Attack above __")
        print("4. Only HP above __")
        print("5. Only names starting with letter(s)")
        print("6. All of them!")
        print("7. Back")
        choice = read_int_safe("Your choice:")
        if choice == 1:
            type = input("Which Type? (e.g. GRASS, WATER):")
            display_pokemon_list([poke for poke in owner_node["pokedex"] if poke["Type"].lower() == type.lower()])
        elif choice == 2:
            display_pokemon_list([poke for poke in owner_node["pokedex"] if poke["Can Evolve"] == "TRUE"])
        elif choice == 3:
            attack_threshold = read_int_safe("Enter Attack threshold:")
            display_pokemon_list([poke for poke in owner_node["pokedex"] if poke["Attack"] > attack_threshold])
        elif choice == 4:
            hp_threshold = read_int_safe("Enter HP threshold:")
            display_pokemon_list([poke for poke in owner_node["pokedex"] if poke["HP"] > hp_threshold])
        elif choice == 5:
            letter_filter = input("Enter letters:")
            display_pokemon_list([poke for poke in owner_node["pokedex"] if poke["Name"].startswith(letter_filter)])
        elif choice == 6:
            display_pokemon_list(owner_node["pokedex"])
        elif choice == 7:
            return


########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex():
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """
    owner_name = input("Enter owner name:")
    owner_node = find_owner_bst(OWNER_ROOT, owner_name)
    if owner_node is None:
        print(f"Owner '{owner_name}' not found.")
        return
    while True:
        print(f"=== {owner_node['owner']}'s Pokedex menu ===")
        print("1. Add Pokemon")
        print("2. Display Pokedex")
        print("3. Release Pokemon")
        print("4. Evolve Pokemon")
        print("5. Back to Main")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            add_pokemon_to_owner(owner_node)
        elif choice == 2:
            display_filter_sub_menu(owner_node)
        elif choice == 3:
            release_pokemon_by_name(owner_node)
        elif choice == 4:
            evolve_pokemon_by_name(owner_node)
        elif choice == 5:
            return

def main_menu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """
    while True:
        print("=== Main Menu ===")
        print("1. New Pokedex")
        print("2. Existing Pokedex")
        print("3. Delete a Pokedex")
        print("4. Display owners by number of Pokemon")
        print("5. Print All")
        print("6. Exit")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            new_pokedex()
        elif choice == 2:
            existing_pokedex()
        elif choice == 3:
            delete_pokedex()
        elif choice == 4:
            sort_owners_by_num_pokemon()
        elif choice == 5:
            print_all_owners()
        elif choice == 6:
            return
        else:
            print("Invalid choice. Please try again.")

def new_pokedex():
    global OWNER_ROOT
    owner_name = input("Enter owner name:")
    print("Choose your starter Pokemon:")
    print("1) Treecko")
    print("2) Torchic")
    print("3) Mudkip")
    first_pokemon = read_int_safe("Your choice:")
    while first_pokemon < 1 or first_pokemon > 3:
        print("Invalid choice. Please try again.")
        first_pokemon = read_int_safe("Your choice:")
    if first_pokemon == 1:
        first_pokemon = HONEN_DATA_BY_NAME["Treecko"]
    elif first_pokemon == 2:
        first_pokemon = HONEN_DATA_BY_NAME["Torchic"]
    elif first_pokemon == 3:
        first_pokemon = HONEN_DATA_BY_NAME["Mudkip"]
    owner_node = create_owner_node(owner_name, first_pokemon)
    OWNER_ROOT = insert_owner_bst(OWNER_ROOT, owner_node)

def delete_pokedex():
    global OWNER_ROOT
    to_delete = input("Enter owner to delete:")
    if find_owner_bst(OWNER_ROOT, to_delete) is None:
        print(f"Owner '{to_delete}' not found.")
        return
    OWNER_ROOT = delete_owner_bst(OWNER_ROOT, to_delete)
    print(f"Deleting {to_delete}'s entire Pokedex...")
    print(f"Pokedex deleted.")


def main():
    """
    Entry point: calls main_menu().
    """
    main_menu()

if __name__ == "__main__":
    main()
