import random   # for quicksort
import time

############### below: binary search tree implementation #############
# I avoided using recursion to prevent stack overflow

class BST_Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert_bst(root: BST_Node, key):
    new_node = BST_Node(key)

    while root is not None:
        if root.key is None:
            root.key = key
            return True
        if key < root.key:
            if root.left is None:
                root.left = new_node
                return True
            root = root.left
        elif key > root.key:
            if root.right is None:
                root.right = new_node
                return True
            root = root.right
        else:
            return False # Ignore insertion for duplicate keys
        

def search_bst(root: BST_Node, key):
    while root is not None and root.key is not None:
        if key < root.key:
            root = root.left
        elif key > root.key:
            root = root.right
        else: # key == root.key
            return root.key
    return None

def _delete_min_bst(node: BST_Node, parent: BST_Node):
    cur = node
    while cur.left is not None:
        parent = cur
        cur = cur.left
    key = cur.key

    cur = None
    parent.left = None

    return key

def _delete_max_bst(node: BST_Node, parent: BST_Node):
    cur = node
    while cur.right is not None:
        parent = cur
        cur = cur.right
    key = cur.key

    cur = None
    parent.right = None

    return key

def delete_bst(root: BST_Node, key):
    if root is None or root.key is None:
        return False
    elif root.key == key:
        root.key = None
        return True 
    
    while root.key != key:
        if key < root.key:
            if root.left is None:
                return False
            elif root.left.key == key:
                if root.left.left is None and root.left.right is None:
                    root.left = None  # Haha I trust the garbage collector
                    return True
            root = root.left
        
        elif key > root.key:
            if root.right is None:
                return False
            elif root.right.key == key:
                if root.right.left is None and root.right.right is None:
                    root.right = None  # Haha I trust the garbage collector
                    return True
            root = root.right
        
        else:
            return False

    else: # key == root.key and there is at least one child
        if root.left is not None:
            root.key = _delete_max_bst(root.left, root)
        elif root.right is not None:
            root.key = _delete_min_bst(root.right, root)
        else:
            return False
        return True
            
def inorder_bst(root: BST_Node):
    result = []
    if root is not None:
        result += inorder_bst(root.left)
        result.append(root.key)
        result += inorder_bst(root.right)
    return result

def preorder_bst(root: BST_Node):
    result = []
    if root is not None:
        result.append(root.key)
        result += preorder_bst(root.left)
        result += preorder_bst(root.right)
    return result

def postorder_bst(root: BST_Node):
    result = []
    if root is not None:
        result += postorder_bst(root.left)
        result += postorder_bst(root.right)
        result.append(root.key)
    return result


################ below: hash table implementations ##################

class ChainingNode:
    def __init__(self, key):
        self.key = key
        self.next_node = None

class HashTable:
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.table = [None] * self.N

        # used to generate a universal hash family
        def get_good_prime(n):
            def is_prime(x):
                if x < 2:
                    return False
                for i in range(2, int(x**0.5) + 1):
                    if x % i == 0:
                        return False
                return True
            prime = n + 1
            while not is_prime(prime):
                prime += 1
            return prime
        self.p = get_good_prime(self.M)
        self.a = random.randint(1, self.p-1)
        self.b = random.randint(1, self.p-1)

    def my_hash(self, key):
        key = (self.a * key + self.b) % self.p
        return key % self.N

def insert_hash(hash_table: HashTable, key):
    idx = hash_table.my_hash(key)
    new_node = ChainingNode(key)

    node = hash_table.table[idx]
    if node is None:
        hash_table.table[idx] = new_node
        return
    else:
        while node.next_node is not None:
            if node.key == key: # Ignore insertion for duplicate keys
                return
            node = node.next_node

        node.next_node = new_node

def search_hash(hash_table: HashTable, key):
    idx = hash_table.my_hash(key)
    node = hash_table.table[idx]
    while node is not None:
        if node.key == key:
            return node.key
        node = node.next_node
    return None

def delete_hash(hash_table: HashTable, key):
    idx = hash_table.my_hash(key)
    node = hash_table.table[idx]
    prev_node = None
    while node is not None:
        if node.key == key:
            if prev_node is None:
                hash_table.table[idx] = node.next_node
            else:
                prev_node.next_node = node.next_node
            return True
        prev_node = node
        node = node.next_node
    return False


############ below: I/O helper functions #############

def read_input(filename):   # input_bst.txt, input_hash.txt
    with open(filename) as file:
        lines = file.readlines()
        arr = list(map(int, lines))
        return arr

def read_op(filename):      # op_bst.txt, op_hash.txt
    with open(filename) as file:
        lines = file.readlines()
        ops = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            op, key = parts[0], int(parts[1])
            ops.append((op, key))
        return ops

def write_output_bst(filename, inorder, preorder, postorder, op_results):
    with open(filename, "w") as file:
        file.write("In-order: " + " ".join(map(str, inorder)) + "\n")
        file.write("Pre-order: " + " ".join(map(str, preorder)) + "\n")
        file.write("Post-order: " + " ".join(map(str, postorder)) + "\n")
        for result in op_results:
            file.write(result + "\n")

def write_output_hash(filename, op_results):
    with open(filename, "w") as file:
        for result in op_results:
            file.write(result + "\n")

def build_bst(input_arr):
    bst_root = BST_Node(None)
    for key in input_arr:
        insert_bst(bst_root, key)
    return bst_root

def build_hashtable(input_arr):
    N = len(input_arr)
    M = max(input_arr)
    hash_table = HashTable(N, M)
    for key in input_arr:
        insert_hash(hash_table, key)
    return hash_table


############ below: Main function for testing #############

def Part1():
    # (1) Test Binary Search Tree
    # (1-1) Read input
    print("Reading inputs from 'input.txt' and 'op.txt'...")
    input_arr = read_input("input.txt")
    op_arr = read_op("op.txt")
    print(f"Successfully read {len(input_arr)} inputs and {len(op_arr)} operations.\n")

    
    # (1-2) Create BST and traversals
    bst_root = build_bst(input_arr)
    inorder = inorder_bst(bst_root)
    preorder = preorder_bst(bst_root)
    postorder = postorder_bst(bst_root)

    # (1-3) Perform operations
    time_start_bst = time.process_time()

    op_results = []
    for op, key in op_arr:
        if op == "Search":
            result = search_bst(bst_root, key)
            if result is not None:
                op_results.append(f"{op} {key}: Found")
            else:
                op_results.append(f"{op} {key}: Not Found")
        elif op == "Delete":
            delete_success = delete_bst(bst_root, key)
            if delete_success:
                op_results.append(f"{op} {key}: Deleted")
            else:
                op_results.append(f"{op} {key}: Not Found")
        elif op == "Insert":
            insert_bst(bst_root, key)

    time_end_bst = time.process_time()
    runtime_ms_bst = (time_end_bst - time_start_bst) * 1000
    print(f"operations completed in {runtime_ms_bst:.3f}ms")

    # (1-4) Output to text file
    print("Writing results to 'output_bst.txt'...")
    write_output_bst('output_bst.txt', inorder, preorder, postorder, op_results)

def Part2():
    # (2) Test Hash Table
    # (2-1) Read input
    print("Reading inputs from 'input.txt' and 'op.txt'...")
    input_arr = read_input("input.txt")
    op_arr = read_op("op.txt")
    print(f"Successfully read {len(input_arr)} inputs and {len(op_arr)} operations.\n")

    # (2-2) Create Hash Table
    hash_table = build_hashtable(input_arr)
    
    # (2-3) Perform Operations
    time_start_hash = time.process_time()

    op_results = []
    for op, key in op_arr:
        if op == "Search":
            result = search_hash(hash_table, key)
            if result is not None:
                op_results.append(f"{op} {key}: Found")
            else:
                op_results.append(f"{op} {key}: Not Found")
        elif op == "Delete":
            delete_success = delete_hash(hash_table, key)
            if delete_success:
                op_results.append(f"{op} {key}: Deleted")
            else:
                op_results.append(f"{op} {key}: Not Found")
        elif op == "Insert":
            insert_hash(hash_table, key)
    
    time_end_hash = time.process_time()
    runtime_ms_hash = (time_end_hash - time_start_hash) * 1000
    print(f"operations completed in {runtime_ms_hash:.3f}ms")

    # (2-4) Output to text file
    print("Writing results to 'output_hash.txt'...")
    write_output_hash('output_hash.txt', op_results)


import os

def Part3():
    # (3-1) Create temporary directory for performance comparison
    if not os.path.exists('tests'):
        os.mkdir('tests')

    # (3-2) Generate test cases
    print("Generating test cases...")
    size = 5000

    # (3-2-1) random
    arr = random.sample(range(1, size * 10), size)
    ops = []
    for _ in range(100):
        ops.append(f"Search {random.randint(1, size * 10)}")
    for _ in range(100):
        ops.append(f"Insert {random.randint(1, size * 10)}")
    for _ in range(100):
        ops.append(f"Delete {random.randint(1, size * 10)}")
        
    with open(f'tests/input_random.txt', 'w') as file:
        for num in arr:
            file.write(f"{num}\n")
    with open(f'tests/op_random.txt', 'w') as file:
        for op in ops:
            file.write(f"{op}\n")

    # (3-2-2) sorted
    arr.sort()
    with open(f'tests/input_sorted.txt', 'w') as file:
        for num in arr:
            file.write(f"{num}\n")
    with open(f'tests/op_sorted.txt', 'w') as file:
        for op in ops:
            file.write(f"{op}\n")

    arr = random.sample(range(1, size * 10), size)
    # (3-3-3) duplicates
    for _ in range(size//5): # make 40% duplicates
        dup = random.choice(arr)
        arr[random.choice(range(size))] = dup
    with open(f'tests/input_duplicates.txt', 'w') as file:
        for num in arr:
            file.write(f"{num}\n")
    with open(f'tests/op_duplicates.txt', 'w') as file:
        for op in ops:
            file.write(f"{op}\n")

    # (3-3) Measure performance
    print("Measuring performance...")
    def get_bst_runtime(input_path, op_path):
        input_arr = read_input(input_path)
        op_arr = read_op(op_path)
        op_arr_search = op_arr[:100]
        op_arr_insert = op_arr[100:200]
        op_arr_delete = op_arr[200:300]

        bst_root = build_bst(input_arr)

        runtime_ms = {}
        tests = [
            ("Search", search_bst, op_arr_search),
            ("Insert", insert_bst, op_arr_insert),
            ("Delete", delete_bst, op_arr_delete)
        ]

        for test in tests:
            op_name, func, op_arr_part = test

            time_start = time.process_time()
            for op, key in op_arr_part:
                func(bst_root, key)
            time_end = time.process_time()
            runtime_ms[op_name] = (time_end - time_start) * 1000 / 100

        return runtime_ms
    
    def get_hash_runtime(input_path, op_path):
        input_arr = read_input(input_path)
        op_arr = read_op(op_path)
        op_arr_search = op_arr[:100]
        op_arr_insert = op_arr[100:200]
        op_arr_delete = op_arr[200:300]

        hash_table = build_hashtable(input_arr)

        runtime_ms = {}
        tests = [
            ("Search", search_hash, op_arr_search),
            ("Insert", insert_hash, op_arr_insert),
            ("Delete", delete_hash, op_arr_delete)
        ]

        for test in tests:
            op_name, func, op_arr_part = test

            time_start = time.process_time()
            for op, key in op_arr_part:
                func(hash_table, key)
            time_end = time.process_time()
            runtime_ms[op_name] = (time_end - time_start) * 1000 / 30

        return runtime_ms
    
    runtime_ms = {
        'random': {'bst': [], 'hash': []},
        'sorted': {'bst': [], 'hash': []},
        'duplicates': {'bst': [], 'hash': []}
    }

    print("Writing results to 'performance_summary.txt'...")
    test_c = ['random', 'sorted', 'duplicates']
    for c in test_c:
        input_path = f'tests/input_{c}.txt'
        op_path = f'tests/op_{c}.txt'

        bst_times = get_bst_runtime(input_path, op_path)
        hash_times = get_hash_runtime(input_path, op_path)

        runtime_ms[c]['bst'] = bst_times
        runtime_ms[c]['hash'] = hash_times

    # (3-4) Plotting
    with open('performance_summary.txt', 'w') as file:
        file.write("PERFORMANCE COMPARISON SUMMARY\n")

        for c in test_c:
            file.write("\n")
            file.write(f"BST Search time ({c}): {runtime_ms[c]['bst']['Search']:.6f}ms\n")
            file.write(f"Hash Table Search time ({c}): {runtime_ms[c]['hash']['Search']:.6f}ms\n")
            file.write(f"BST Insert time ({c}): {runtime_ms[c]['bst']['Insert']:.6f}ms\n")
            file.write(f"Hash Table Insert time ({c}): {runtime_ms[c]['hash']['Insert']:.6f}ms\n")
            file.write(f"BST Delete time ({c}): {runtime_ms[c]['bst']['Delete']:.6f}ms\n")
            file.write(f"Hash Table Delete time ({c}): {runtime_ms[c]['hash']['Delete']:.6f}ms\n")
        
if __name__ == "__main__":
    print("============================================")
    print("    4190.407 Algorithms - Homework 3")
    print("    Binary Search Tree and Hash Table")
    print("    Yeonjun Kim / 2024-13755")
    print("============================================")

    # Part 1: Binary Search Tree Test
    print("\n# Part 1")
    Part1()

    # Part 2: Output Hash Test
    print("\n# Part 2")
    Part2()

    # Part 3: Performance Comparison
    print("\n# Part 3")
    Part3()

    exit(0)