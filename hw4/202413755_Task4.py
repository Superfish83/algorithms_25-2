import random, time
import heapq

INF = float('inf')

############################################################
############################################################
# (1) Algorithm Implementations

###### below: Dijkstra and Bellman-Ford implementation #####

# returns distances: list
def dijkstra(graph, s):
    N = len(graph)
    d = [INF] * N
    d[s] = 0

    MAX_IT = N * N
    it_cnt = 0

    pqueue = [(0, s)]  # (distance, node)

    while len(pqueue) > 0:
        it_cnt += 1
        if it_cnt > MAX_IT:
            print("Dijkstra exceeded max iterations (possibly negative cycle?)")
            break

        cur_dist, u = heapq.heappop(pqueue)

        if cur_dist > d[u]:
            continue

        for v, w in graph[u]:
            new_dist_v = cur_dist + w
            if new_dist_v < d[v]:
                d[v] = new_dist_v
                heapq.heappush(pqueue, (new_dist_v, v))

    return d


# returns (distances: list, neg_cycle: bool)
def bellman_ford(graph, s):
    N = len(graph)
    NUM_IT = N
    d = [INF] * N
    d[s] = 0

    neg_cycle = False
    for i in range(NUM_IT):
        d_next = d.copy()

        for u in range(N):
            for v, w in graph[u]:
                new_dist_v = d[u] + w
                if new_dist_v < d_next[v]:
                    d_next[v] = new_dist_v
        if d_next == d:
            break
        elif i == NUM_IT - 1:
            neg_cycle = True
        d = d_next

    return d, neg_cycle


############################################################
############################################################
# (2) I/O helpers, random test case generators

##### below: I/O helper functions #####

# graph is represented as adjacency list
def read_input(filepath='input.txt'):
    with open(filepath) as file:
        lines = file.readlines()

        N, M = map(int, lines[0].split())
        graph = [[] for _ in range(N)]

        for line in lines[1:M+1]:
            u, v, w = map(int, line.split())
            graph[u-1].append((v-1, w))

        s = int(lines[-1].split()[-1]) - 1
        return graph, s

# distances: a list of numbers (including INF)
def write_result(distances, neg_cycle=False, filepath='output.txt'):
    with open(filepath, 'w') as file:
        if neg_cycle:
            file.write("Negative cycle detected\n")
        else:
            for n, dist in enumerate(distances):
                if dist == INF:
                    file.write(f"Node {n+1}: INF\n")
                else:
                    file.write(f"Node {n+1}: {dist}\n")


##### below: Test case generation #####

# generates a random directed graph and writes to filepath
def gen_random_input(N, M, minw=1, maxw=10, filepath='input.txt'):
    graph = [[] for _ in range(N)]
    
    gen_cnt = 0
    while gen_cnt < M:
        u = random.randint(0, N-1)
        v = random.randint(0, N-1)
        w = random.randint(minw, maxw)

        # avoid self-loops and duplicate edges
        if u != v and v not in [edge[0] for edge in graph[u]]:
            graph[u].append((v, w))
            gen_cnt += 1

    s = random.randint(0, N-1)

    with open(filepath, 'w') as file:
        file.write(f"{N} {M}\n")
        for u in range(N):
            for v, w in graph[u]:
                file.write(f"{u} {v} {w}\n")
        file.write(f"Source: {s}\n")

############################################################
############################################################
# (3) Functions that test and measure runtime of algorithms

##### below: Test functions #####
def test_dijkstra(input_path='input.txt', output_path='output.txt'):
    graph, s = read_input(input_path)

    time_start = time.process_time()
    d = dijkstra(graph, s)
    time_end = time.process_time()

    write_result(d, False, output_path)
    runtime_ms = (time_end - time_start) * 1000

    return runtime_ms


def test_bellman_ford(input_path='input.txt', output_path='output.txt'):
    graph, s = read_input(input_path)

    time_start = time.process_time()
    d, neg_cycle = bellman_ford(graph, s)
    time_end = time.process_time()

    write_result(d, neg_cycle, output_path)
    runtime_ms = (time_end - time_start) * 1000

    return runtime_ms


############################################################
############################################################
# (4) Main function

if __name__ == "__main__":
    print("============================================")
    print("    4190.407 Algorithms - Homework 4")
    print("    Shortest Path Algorithms")
    print("    Yeonjun Kim / 2024-13755")
    print("============================================")

    # Part 1: Test example case
    print("\n# Part 1")
    print("Testing Dijkstra and Bellman-Ford Algorithms for example case...")

    test_dijkstra('input.txt', 'output_d.txt')
    test_bellman_ford('input.txt', 'output_bf.txt')

    print("Results written to 'output_d.txt' and 'output_bf.txt'.")

    # Part 2: Test large random case and measure runtime
    print("\n# Part 2")
    print("Generating random test case for Bellman-Ford Algorithm...")
    print("Testing Dijkstra and Bellman-Ford Algorithms...")

    gen_random_input(1000, 5000, 1, 10, 'input_random.txt')
    t1 = test_dijkstra('input_random.txt', 'output_d_random.txt')
    t2 = test_bellman_ford('input_random.txt', 'output_bf_random.txt')

    print(f"Runtime for first test: {t1:.3f} ms")
    print(f"Runtime for second test: {t2:.3f} ms")

    print("Results written to 'output_d_random.txt' and 'output_bf_random.txt'.")

    exit(0)