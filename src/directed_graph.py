#!/usr/bin/env python3
import undirected_graph
from sys import stdin
from copy import deepcopy, copy
from queue import Queue, LifoQueue
from collections import deque
  

inf = 1000000007

def readAsEdgeList(file = stdin, test_emptiness = True):
  ''' unpack graph as (n, m, e) = readAsEdgeList(file) '''
  n, m = map(int, file.readline().split())
  
  if test_emptiness and n == 0:
    fout.write('Graph is empty! Exit!\n')
    sys.exit(2)
  
  E = [tuple(map(int, file.readline().split())) for i in range(m)]
  return n, m, E

def incidentMatrixByEdgeList(G):
  # 1 - index
  n, m, E = G
  matrix = [[0] * m for i in range(n)]
  for (i, e) in enumerate(E):
    (v1, v2) = e
    if v1 == v2:
      matrix[v1-1][i] = 2
    else:
      matrix[v1 - 1][i] = -1
      matrix[v2 - 1][i] = +1
  return matrix

def adjacencyMatrixByEdgeList(G):
  # 1 - index
  n, m, E = G
  matrix = [[0] * n for i in range(n)]
  for (v1, v2) in E:
    matrix[v1-1][v2-1] += 1
  return matrix

def inOutDegreesByEdgeList(G):
  # 1 - index
  n, m, E = G
  inD, outD = [0] * n, [0] * n
  for (v1, v2) in E:
    outD[v1-1] += 1
    inD[v2-1]  += 1
  return inD, outD

def edgeListToAdjacencyList(G):
  # Note: also converted from 1-index to 0-index 
  n, m, E = G
  adj_lst = [[] for i in range(n)]
  for (v1, v2) in E:
    adj_lst[v1-1].append(v2-1)
  return (n, m, adj_lst)

def wavingDistance(G):
  # 0 -index, adj_list repr
  n, m, V = G
  D = [0] * n
  for i in range(n):
    D[i] = dist1ToAll(G, i)
  return D

def dist1ToAll(G, i):
  # 0 - index, adj_list repr
  n, m, V = G
  d = [inf] * n
  d[i] = 0
  q = Queue()
  q.put(i)
  while not q.empty():
    v = q.get()
    for adj in V[v]:
      if d[adj] == inf:
        d[adj] = d[v] + 1
        q.put(adj)
  return d

def wavingReachable(G):
  # 0 -index, adj_list repr
  n, m, V = G
  R = [0] * n
  for i in range(n):
    R[i] = reachable1ToAll(G, i)
  return R

def reachable1ToAll(G, i):
  # 0 - index, adj_list repr
  n, m, V = G
  r = [0] * n
  q = Queue()
  q.put(i)
  r[i] = 1
  while not q.empty():
    v = q.get()
    for adj in V[v]:
      if r[adj] == 0:
        r[adj] = 1
        q.put(adj)
  return r

def get_loops(G, limit = 10):

  def visit(i):
    state[i] = 1
    for v in V[i]:
      if par[v] == -1:
        par[v] = i
      if state[v] == 0:
        visit(v)
      elif state[v] == 1 and len(loops) < limit:
        loop = [v]
        c = i
        while c != v:
          loop.append(c)
          c = par[c]
        loop.reverse()
        loop.append(loop[0])
        loops.append(loop)
    state[i] = 2 
    

  # 0-index, adj_list repr
  n, m, V = G
  loops = []
  state = [0] * n # 0 - unmarked, 1 - tmp, 2 - finished
  par = [-1] * n # number of vertex parent
  for i in range(n):
    if par[i] == -1:
      visit(i)
  return loops

def isStronglyConnectedByRMatrix(R):
  return all(all(row[:i]) and all(row[i+1:]) for i, row in enumerate(R))
  
def isOneSideConnectedByRMatrix(R):
  n = len(R)
  return all(R[i][j] or R[j][i] or i == j for i in range(n) for j in range(n))

def isWeaklyConnectedByEdgeList(G):
  return undirected_graph.isConnectedByEdgeList(G)

def floydWarshall(M):
  # 0 - index, matrix repr
  n = len(M)
  D = deepcopy(M)
  for k in range(n):
    for i in range(n):
      for j in range(n):
        if M[i][k] and M[k][j]:
          D[i][j] = min(D[i][j], D[i][k] + D[k][j])
  return D

def bfs_table(G, s):
  # adjacency list representation
  n, m, V = G
  result = []
  visited = [False] * n
  visited[s] = True
  q = deque()
  q.append(s)
  for i in range(n):
    v = q.popleft()
    for neighbour in V[v]:
      if not visited[neighbour]:
        visited[neighbour] = True
        q.append(neighbour)
    result.append((i+1, v+1, list([a+1 for a in q])))
  return result

def dfs_table(G, s):
  # adjacency list representation
  n, m, V = G
  result = []
  visited = [False] * n
  visited[s] = True
  stack = []
  stack.append(s)
  for i in range(n):
    v = stack.pop()
    for neighbour in V[v]:
      if not visited[neighbour]:
        visited[neighbour] = True
        stack.append(neighbour)
    result.append((i+1, v+1, str([a+1 for a in stack])))
  return result

def topological_sort(G):
  ''' adjacency list representation '''
  def visit(i):
    state[i] = temporary
    for v in V[i]:
      if state[v] == unmarked:
        if not visit(v):
          return False
      elif state[v] == temporary:
        return False
    state[i] = finished
    result.append(i)
    return True 

  # 0-index, adj_list repr
  n, m, V = G
  unmarked, temporary, finished = 0, 1, 2
  state = [unmarked] * n
  result = []
  for i in range(n):
    if state[i] == unmarked:
      if not visit(i):
        return None
  return list(reversed([v+1 for v in result]))


def reverse(G):
  ''' adjacency list representation '''
  n, m, V = G
  V_rev = [[] for i in range(n)]
  for i, l in enumerate(V):
    for v in l:
      V_rev[v].append(i)
  return (n, m, V_rev)

def strong_components(G):
  def visit(s):
    visited[s] = True
    for v in V[s]:
      if not visited[v]:
        visit(v)
    S.append(s)

  n, m, V = G
  visited = [False] * n
  S = []
  for i in range(n):
    if not visited[i]:
      visit(i)



  def visitReverse(s):
    components[-1].append(s + 1)
    visited[s] = True
    for v in V_rev[s]:
      if not visited[v]:
        visitReverse(v)

  V_rev = reverse(G)[2]
  visited = [False] * n
  components = []
  for i in range(n):
    cur = S.pop()
    if not visited[cur]:
      components.append([])
      visitReverse(cur)

  return components