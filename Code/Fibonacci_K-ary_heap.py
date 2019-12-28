from collections import defaultdict
from heapq import *
import random
import time
from fibHeap import FibonacciHeap


def dijkstra_using_k_array_heaps(edges, f, t):
    count = 0
    dict = defaultdict(list)
    for left, right, given_c in edges:
        dict[left].append((given_c, right))
    hp, visited, min_cost = [(0, f, ())], set(), {f: 0}
    while hp:
        (cost, v1, path) = heappop(hp)
        if v1 not in visited:
            visited.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, count)
            count += 1

            for given_c, v2 in dict.get(v1, ()):
                if v2 in visited: continue
                prev = min_cost.get(v2, None)
                next = cost + given_c
                if prev is None or next < prev:
                    min_cost[v2] = next
                    heappush(hp, (next, v2, path))
                    # here we can see that number of times element gets added can be used to decide the performance ~ number of times decrease key is called.
    return float("inf")


def generateAdjListFromData(edges, n):
    adjList = [[] for k in range(n + 1)]
    for edge in edges:
        s, d, w = edge[0], edge[1], edge[-1]
        adjList[s].append((d, w))
    return adjList


def dijkstra_using_fiboHeap(adjList, source, dest, sink=None):
    n = len(adjList)  # intentionally 1 more than the number of vertices, keep the 0th entry free for convenience
    visited = [False] * n
    distance = [float('inf')] * n

    heapNodes = [None] * n
    heap = FibonacciHeap()
    for i in range(1, n):
        heapNodes[i] = heap.insert(float('inf'), i)  # distance, label

    distance[source] = 0
    heap.decrease_key(heapNodes[source], 0)
    calls = 0
    while heap.total_nodes:
        if heap.find_min():
            current = heap.extract_min().value
            visited[current] = True

            # early exit
            if sink and current == sink:
                break

            for (neighbor, cost) in adjList[current]:
                if not visited[neighbor]:
                    if distance[current] + cost < distance[neighbor]:
                        distance[neighbor] = distance[current] + cost
                        heap.decrease_key(heapNodes[neighbor], distance[neighbor])
                        calls += 1
                        if dest == neighbor:
                            return distance[dest]
        else:
            return distance[dest]

    return distance[dest]


def myFibo(edges, n, a, b):
    aa = dijkstra_using_fiboHeap(generateAdjListFromData(edges, n), a, b)
    return aa


f = open('graph_input')
karry = open('graph_output', 'w')
fibo = open('graph_output_fibo', 'w')

inp = f.readline().strip()
while inp:
    n, e = map(int, inp.split())
    edges = []
    nodestart = []
    for x in range(e):
        arr = [int(x) for x in f.readline().strip().split()]
        edges.append((arr[0], arr[1], arr[-1]))
        nodestart.append(arr[0])
    # taking random starting and ending points and making sure they are not the same
    a = -1
    b = -1
    while a == b:
        a = random.choice(nodestart)
        b = random.choice(nodestart)

    stime = time.time()
    ans = dijkstra_using_k_array_heaps(edges, a, b)
    etime = time.time() - stime
    stime = time.time()
    ans1 = myFibo(edges, n, a, b)
    etime1 = time.time()-stime

    fibotime = etime1*1000
    karytime = etime*1000

    karry.write(str(n) + "," + str(karytime) + "\n")
    fibo.write(str(n) + "," + str(fibotime) + "\n")
    inp = f.readline().strip()

karry.close()
fibo.close()
f.close()
