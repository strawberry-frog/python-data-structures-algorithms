#modified by Katherine Botticelli 

class Stack(list):          # Use list to define Stack class
    def push(self, item): self.append(item) # push == append
    def peek(self): return self[-1] # Last element is top of stack
    def isEmpty(self): return len(self) == 0
    
class Vertex(object):        # A vertex in a graph
    def __init__(self, name): # Constructor: stores a vertex name
        self.name = name       # Store the name

    def __str__(self):        # Summarize vertex in a string
        return '<Vertex {}>'.format(self.name)
    
class Graph(object):         # A graph containing vertices and edges
    def __init__(self):       # Constructor
        self._vertices = []    # A list/array of vertices
        self._adjMat = {}      # A hash table mapping vertex pairs to 1

    def nVertices(self):      # Get the number of graph vertices, i.e.
        return len(self._vertices) # the length of the vertices list

    def nEdges(self):         # Get the number of graph edges by
      return len(self._adjMat) // 2 # dividing the # of keys by 2

    def addVertex(self, vertex): # Add a new vertex to the graph
        self._vertices.append(vertex) # Place at end of vertex list

    def validIndex(self, n):  # Check that n is a valid vertex index
        if n < 0 or self.nVertices() <= n: # If it lies outside the
            raise IndexError    # valid range, raise an exception
        return True            # Otherwise it's valid

    def getVertex(self, n):   # Get the nth vertex in the graph
        if self.validIndex(n): # Check that n is a valid vertex index
            return self._vertices[n] # and return nth vertex

    def addEdge(self, A, B):  # Add an edge between two vertices A & B
        self.validIndex(A)     # Check that vertex A is valid
        self.validIndex(B)     # Check that vertex B is valid
        if A == B:             # If vertices are the same
            raise ValueError    # raise exception
        self._adjMat[A, B] = 1 # Add edge in one direction and
        self._adjMat[B, A] = 1 # the reverse direction

    def hasEdge(self, A, B):  # Check for edge between vertices A & B
        self.validIndex(A)     # Check that vertex A is valid
        self.validIndex(B)     # Check that vertex B is valid
        return self._adjMat.get( # Look in adjacency matrix hash table
            (A, B), False)      # Return either the edge count or False
    
    def vertices(self):      # Generate sequence of all vertex indices
        return range(self.nVertices()) # Same as range up to nVertices
    
    def adjacentVertices(    # Generate a sequence of vertex indices
            self, n):          # that are adjacent to vertex n
        self.validIndex(n)    # Check that vertex n is valid
        for j in range(len(self.vertices())): # Loop over all other vertices
            if j != n and self.hasEdge(n, j): # If other vertex connects
                yield j         # via edge, yield other vertex index

    def adjacentUnvisitedVertices( # Generate a sequence of vertex
            self, n,           # indices adjacent to vertex n that do
            visited,           # not already show up in the visited list
            markVisits=True):  # and mark visits in list, if requested
        for j in self.adjacentVertices(n): # Loop through adjacent
            
            if not visited[j]: # vertices, check visited
                if markVisits:  # flag, and if unvisited, optionally
                    visited[j] = True # mark the visit
                yield j         # and yield the vertex index 
                    
    def depthFirst(          # Traverse the vertices in depth-first
            self, n):          # order starting at vertex n
        self.validIndex(n)    # Check that vertex n is valid
        visited = [False] * self.nVertices() # Nothing visited initially
        stack = Stack()       # Start with an empty stack
        stack.push(n)         # and push the starting vertex index on it
        visited[n] = True     # Mark vertex n as visited
        yield (n, stack)      # Yield initial vertex and initial path
        while not stack.isEmpty(): # Loop until nothing left on stack
            visit = stack.peek() # Top of stack is vertex being visited
            adj = None
            for j in self.adjacentUnvisitedVertices( # Loop over adjacent
                visit, visited): # vertices marking them as we visit them
                adj = j         # Next vertex is first adjacent unvisited
                break           # one, and the rest will be visited later
            if adj is not None: # If there's an adjacent unvisited vertex
                stack.push(adj) # Push it on stack and
                yield (adj, stack) # yield it with the path leading to it
            else:              # Otherwise we're visiting a dead end so
                stack.pop()     # pop the vertex off the stack
                
    def minimumSpanningTree( # Compute a minimum spanning tree
            self, n):          # starting at vertex n
        self.validIndex(n)    # Check that vertex n is valid
        tree = Graph()        # Initial MST is an empty graph
        vMap = [None] * self.nVertices() # Array to map vertex indices
        for vertex, path in self.depthFirst(n):
            vMap[vertex] = tree.nVertices() # DF visited vertex will be
            tree.addVertex(    # last vertex in MST as we add it
                self.getVertex(vertex))
            if len(path) > 1:  # If the path has more than one vertex,
                tree.addEdge(   # add last edge in path to MST, mapping
                vMap[path[-2]], vMap[path[-1]]) # vertex indices
        return tree
    
    def predecessorVertices( # Generate a sequence of vertex indices
            self, n):          # that are adjacent predecessors to n
        self.validIndex(n)    # Check that vertex index n is valid
        for j in range(self.vertices()): # Loop over all other vertices
            if j != n and self.hasEdge(j, n): # If other vertex connects
                yield j         # via edge, yield other vertex index

    def onlyVisitedPredecessors( # Test whether vertex n's predecessors
            self, n, visited): # have all been visited, if any
        return all(visited[j] # All predecessors must have been set in
                    for j in self.predecessorVertices(n)) # visited array

    def findUnvisitedWithoutPredecessor( # Find a vertex without
            self, visited):    # unvisited predecessor vertices, if any
        for vertex in self.vertices(): # Loop over all vertices
            if (not visited[vertex] and # If vertex is unvisited and has
                self.onlyVisitedPredecessors( # only visited
                    vertex, visited)): # predecessors,
                return vertex   # then return it
        return None           # Otherwise there's a cycle or no vertices

    def sortVerticesTopologically( # Return a sequence of all vertex
            self):             # indices sorted topologically
        result = []           # Result list of vertices
        nVertices = self.nVertices() # Number of vertices
        visited = [None] * nVertices # Array to mark visited vertices
        while len(result) < nVertices: # Loop until all vertices handled
            vertex = self.findUnvisitedWithoutPredecessor( # Find an
                visited)     # unvisited vertex without predecessors
            if vertex is None: # If no such vertex exists, then raise an
                raise Exception('Cycle in graph, cannot sort') # exception
            result.append(vertex) # Append unvisited vertex and
            visited[vertex] = True # mark it as visited
        return result
    
    def degree(self, n):     # Get degree of vertex as (in, out) pair
        self.validIndex(n)    # Validate vertex index
        inb, outb = 0, 0      # Count inbound and outbound edges
        for j in self.vertices(): # Loop over all vertices
            if j != n:         # other than target vertex
                if self.hasEdge(j, n): # If other vertex precedes
                    inb += 1            # increase inbound degree
                if self.hasEdge(n, j): # If other vertex succeeds n
                    outb += 1           # increase outbound degree
        return (inb, outb)    # Return inbound and outbound degree

    def sortVertsTopologically( # Return sequence of all vertex indices
            self):             # sorted topologically more efficiently
        vertsByDegree = [     # Make an empty hash table for every
            {} for j in range( # possible degree, max = nVerts – 1 or
                min(self.nVertices(), self.nEdges() + 1))] # nEdges
        inDegree = [0] * self.nVertices() # Allocate indegree array
        for vertex in self.vertices(): # Loop over all vertices, record
            inDegree[vertex] = self.degree(vertex)[0] # inbound degree
            vertsByDegree[     # In hash table for this inbound degree
                inDegree[vertex]][vertex] = 1 # insert vertex
        result = []           # Result list is initially empty
        while len(            # While there are vertices with inbound
                vertsByDegree[0]) > 0: # degree of 0
            vertex, _ = vertsByDegree[0].popitem() # take vertex out of
            result.append(vertex) # hash table & add it to end of result
            for s in self.adjacentVertices( # Loop over vertex's
                vertex):     # successors; move them to lower degree
                vertsByDegree[ # In hash table holding successor vertex
                inDegree[s]].pop(s) # delete the successor
                inDegree[s] -= 1 # Decrease inbound degree of successor
                vertsByDegree[ # In hash table for lowered inbound degree
                inDegree[s]][s] = 1 # insert modified successor
        if len(result) == self.nVertices(): # All vertices in result?
            return result      # Yes, then return it, otherwise cycle
        raise Exception('Cycle in graph, cannot sort')
# 2nd Attempt 
    def clique(self, N): #finds all cliques in the graph 
        
        for k in range(self.nVertices()): # loops through all the vertices
            for i in range(self.nVertices()): # loops through all the vertices 
                clique = []                    # creates a clique array 
                clique.append(k)               # appends k to clique to start the clique 
                if i == 0 and  k == 0:         # if i = k 
                    for j in range(self.nVertices()): # loop through vertices
                        if i == j or j == k:  # if i = j and j = k 
                            clique = clique   # do nothing 
                        elif self._adjMat[i,j] == 1: # else if matrix at i, j is 1 
                            # check that the last item in clique and j are 1 
                            if self._adjMat[clique[len(clique)-1], j] == 1:
                                clique.append(j)        # if clique is a clique then append 
                        
                            if len(clique) == N and self._adjMat[clique[0], j] == 1: # if clique is length N and is a clique 
                                yield clique # yield clique 
                                clique.remove(clique[len(clique) - 1]) # clique remove last clique item 
            
                elif k == i:   # if i = k then 
                    clique = clique # do nothing 
                elif k == 0 and i == 1: # if k = 0 and i = 1 
                    clique = clique # do nothing 
                elif self._adjMat[k,i] == 1: # if k, i are 1 in the matrix 
                    clique.append(i) # append i to clique 
                    for j in range(self.nVertices()): # loop through vertices
                        if i == j or j == k:  # if i = j and j = k 
                            clique = clique   # do nothing 
                        elif self._adjMat[i,j] == 1: # else if matrix at i, j is 1 
                            # check that the last item in clique and j are 1 
                            if self._adjMat[clique[len(clique)-1], j] == 1:
                                clique.append(j)        # if clique is a clique then append 
                        
                            if len(clique) == N and self._adjMat[clique[0], j] == 1: # if clique is length N and is a clique 
                                yield clique # yield clique 
                                clique.remove(clique[len(clique) - 1]) # clique remove last clique item 


    def __str__(self):       # Summarize the graph in a string
        nVertices = self.nVertices()
        nEdges = self.nEdges()
        return '<Graph of {} vert{} and {} edge{}>'.format(
            nVertices, 'ex' if nVertices == 1 else 'ices',
            nEdges, '' if nEdges == 1 else 's')

    def print(self,          # Print all the graph's vertices and edges
                prefix=''):    # Prefix each line with the given string
        print('{}{}'.format(prefix, self)) # Print summary form of graph
        for vertex in self.vertices(): # Loop over all vertex indices
            print('{}{}:'.format(prefix, vertex), # Print vertex index
                self.getVertex(vertex)) # and string form of vertex
            for k in range(vertex + 1, self.nVertices()): # Loop over
                if self.hasEdge(vertex, k): # higher vertex indices, if
                    print(prefix, # there's an edge to it, print edge
                        self._vertices[vertex].name,
                        '<->',
                        self._vertices[k].name)
    def matrixFirstCondition(self):
        #five vertices fully interconnected 
        self.addVertex(Vertex('A'))
        self.addVertex(Vertex('B'))
        self.addVertex(Vertex('C'))
        self.addVertex(Vertex('D'))
        self.addVertex(Vertex('E'))
        self.addVertex(Vertex('F'))
        self.addVertex(Vertex('G'))
        self.addVertex(Vertex('H'))
        self.addVertex(Vertex('I'))
    
        self._adjMat[0,0] = 0
        self._adjMat[0,1] = 1
        self._adjMat[0,2] = 1
        self._adjMat[0,3] = 1
        self._adjMat[0,4] = 1
        self._adjMat[0,5] = 0
        self._adjMat[0,6] = 0
        self._adjMat[0,7] = 0
        self._adjMat[0,8] = 0
        self._adjMat[0,9] = 1
        self._adjMat[1,0] = 1
        self._adjMat[1,1] = 1
        self._adjMat[1,2] = 1
        self._adjMat[1,3] = 1
        self._adjMat[1,4] = 1
        self._adjMat[1,5] = 0
        self._adjMat[1,6] = 0
        self._adjMat[1,7] = 0
        self._adjMat[1,8] = 0
        self._adjMat[1,9] = 0
        
        self._adjMat[2,0] = 1
        self._adjMat[2,1] = 1
        self._adjMat[2,2] = 0
        self._adjMat[2,3] = 1
        self._adjMat[2,4] = 1
        self._adjMat[2,5] = 0
        self._adjMat[2,6] = 0
        self._adjMat[2,7] = 0
        self._adjMat[2,8] = 0
        self._adjMat[2,9] = 0

        self._adjMat[3,0] = 1
        self._adjMat[3,1] = 1
        self._adjMat[3,2] = 1
        self._adjMat[3,3] = 0
        self._adjMat[3,4] = 1
        self._adjMat[3,5] = 0
        self._adjMat[3,6] = 0
        self._adjMat[3,7] = 0
        self._adjMat[3,8] = 0
        self._adjMat[3,9] = 0
        
        
        self._adjMat[4,0] = 1
        self._adjMat[4,1] = 1
        self._adjMat[4,2] = 1
        self._adjMat[4,3] = 1
        self._adjMat[4,4] = 0
        self._adjMat[4,5] = 0
        self._adjMat[4,6] = 0
        self._adjMat[4,7] = 0
        self._adjMat[4,8] = 0
        self._adjMat[4,9] = 0

        self._adjMat[5,0] = 0
        self._adjMat[5,1] = 0
        self._adjMat[5,2] = 0
        self._adjMat[5,3] = 0
        self._adjMat[5,4] = 0
        self._adjMat[5,5] = 0
        self._adjMat[5,6] = 1
        self._adjMat[5,7] = 0
        self._adjMat[5,8] = 0
        self._adjMat[5,9] = 0
        
        self._adjMat[6,0] = 0
        self._adjMat[6,1] = 0
        self._adjMat[6,2] = 0
        self._adjMat[6,3] = 0
        self._adjMat[6,4] = 0
        self._adjMat[6,5] = 1
        self._adjMat[6,6] = 0
        self._adjMat[6,7] = 0
        self._adjMat[6,8] = 0
        self._adjMat[6,9] = 0
        
        self._adjMat[7,0] = 0
        self._adjMat[7,1] = 0
        self._adjMat[7,2] = 0
        self._adjMat[7,3] = 0
        self._adjMat[7,4] = 0
        self._adjMat[7,5] = 0
        self._adjMat[7,6] = 0
        self._adjMat[7,7] = 0
        self._adjMat[7,8] = 1
        self._adjMat[7,9] = 0
        
        self._adjMat[8,0] = 0
        self._adjMat[8,1] = 0
        self._adjMat[8,2] = 0
        self._adjMat[8,3] = 0
        self._adjMat[8,4] = 0
        self._adjMat[8,5] = 0
        self._adjMat[8,6] = 0
        self._adjMat[8,7] = 1
        self._adjMat[8,8] = 0
        self._adjMat[8,9] = 0
        
        self._adjMat[9,0] = 1
        self._adjMat[9,1] = 0
        self._adjMat[9,2] = 0
        self._adjMat[9,3] = 0
        self._adjMat[9,4] = 0
        self._adjMat[9,5] = 0
        self._adjMat[9,6] = 0
        self._adjMat[9,7] = 0
        self._adjMat[9,8] = 0
        self._adjMat[9,9] = 0
        
        
        for i in range(self.nVertices()):                # loops through the vertices 
            print("[", end = " ")
            for j in range(self.nVertices()):
                    print( self._adjMat[i,j], end = " ")  
            print("]")
        self._adjMat = self._adjMat
        
    def matrixSecondCondition(self):
        #three overlapping cliques size 4 
        self.addVertex(Vertex('K'))
        self.addVertex(Vertex('L'))
        self.addVertex(Vertex('M'))
        self.addVertex(Vertex('N'))
        self.addVertex(Vertex('O'))
        self.addVertex(Vertex('P'))
        self.addVertex(Vertex('Q'))
        self.addVertex(Vertex('R'))
        self.addVertex(Vertex('S'))
        self.addVertex(Vertex('T'))
        self._adjMat[0,0] = 0
        self._adjMat[0,1] = 1
        self._adjMat[0,2] = 1
        self._adjMat[0,3] = 1
        self._adjMat[0,4] = 1
        self._adjMat[0,5] = 0
        self._adjMat[0,6] = 0
        self._adjMat[0,7] = 0
        self._adjMat[0,8] = 1
        self._adjMat[0,9] = 0
        
        self._adjMat[1,0] = 1
        self._adjMat[1,1] = 0
        self._adjMat[1,2] = 0
        self._adjMat[1,3] = 0
        self._adjMat[1,4] = 0
        self._adjMat[1,5] = 0
        self._adjMat[1,6] = 0
        self._adjMat[1,7] = 0
        self._adjMat[1,8] = 0
        self._adjMat[1,9] = 1
        
        self._adjMat[2,0] = 1
        self._adjMat[2,1] = 0
        self._adjMat[2,2] = 0
        self._adjMat[2,3] = 0
        self._adjMat[2,4] = 0
        self._adjMat[2,5] = 0
        self._adjMat[2,6] = 0
        self._adjMat[2,7] = 0
        self._adjMat[2,8] = 0
        self._adjMat[2,9] = 1

        self._adjMat[3,0] = 1
        self._adjMat[3,1] = 0
        self._adjMat[3,2] = 0
        self._adjMat[3,3] = 0
        self._adjMat[3,4] = 0
        self._adjMat[3,5] = 1
        self._adjMat[3,6] = 0
        self._adjMat[3,7] = 0
        self._adjMat[3,8] = 0
        self._adjMat[3,9] = 0
        
        
        self._adjMat[4,0] = 1
        self._adjMat[4,1] = 0
        self._adjMat[4,2] = 0
        self._adjMat[4,3] = 0
        self._adjMat[4,4] = 0
        self._adjMat[4,5] = 0
        self._adjMat[4,6] = 0
        self._adjMat[4,7] = 0
        self._adjMat[4,8] = 0
        self._adjMat[4,9] = 0

        self._adjMat[5,0] = 0
        self._adjMat[5,1] = 0
        self._adjMat[5,2] = 0
        self._adjMat[5,3] = 1
        self._adjMat[5,4] = 0
        self._adjMat[5,5] = 0
        self._adjMat[5,6] = 0
        self._adjMat[5,7] = 0
        self._adjMat[5,8] = 1
        self._adjMat[5,9] = 0
        
        self._adjMat[6,0] = 1
        self._adjMat[6,1] = 0
        self._adjMat[6,2] = 0
        self._adjMat[6,3] = 0
        self._adjMat[6,4] = 0
        self._adjMat[6,5] = 0
        self._adjMat[6,6] = 0
        self._adjMat[6,7] = 1
        self._adjMat[6,8] = 0
        self._adjMat[6,9] = 0
        
        self._adjMat[7,0] = 0
        self._adjMat[7,1] = 0
        self._adjMat[7,2] = 0
        self._adjMat[7,3] = 0
        self._adjMat[7,4] = 1
        self._adjMat[7,5] = 0
        self._adjMat[7,6] = 1
        self._adjMat[7,7] = 0
        self._adjMat[7,8] = 0
        self._adjMat[7,9] = 0
        
        self._adjMat[8,0] = 1
        self._adjMat[8,1] = 0
        self._adjMat[8,2] = 0
        self._adjMat[8,3] = 0
        self._adjMat[8,4] = 0
        self._adjMat[8,5] = 1
        self._adjMat[8,6] = 0
        self._adjMat[8,7] = 0
        self._adjMat[8,8] = 0
        self._adjMat[8,9] = 0
        
        self._adjMat[9,0] = 0
        self._adjMat[9,1] = 0
        self._adjMat[9,2] = 1
        self._adjMat[9,3] = 0
        self._adjMat[9,4] = 0
        self._adjMat[9,5] = 0
        self._adjMat[9,6] = 0
        self._adjMat[9,7] = 0
        self._adjMat[9,8] = 0
        self._adjMat[9,9] = 0
        
        
        for i in range(self.nVertices()):                # loops through the vertices 
            print("[", end = " ")
            for j in range(self.nVertices()):
                    print( self._adjMat[i,j], end = " ")  
            print("]")
        self._adjMat = self._adjMat
        

# interconnected graph 
graph = Graph()
graph.matrixFirstCondition()
for clique in graph.clique(3):
    print(clique)
    
for clique in graph.clique(4):
    print(clique)
for clique in graph.clique(5):
    print(clique)

# graph with cliques of size 4 and all connected to A

newGraph = Graph()
newGraph.matrixSecondCondition()

for newClique in newGraph.clique(3):
    print(newClique)
    
for newClique in newGraph.clique(4):
    print(newClique)
    
for newClique in newGraph.clique(5):
    print(newClique)

#Lafore, Robert; Broder, Alan; Canning, John. Data Structures & Algorithms in Python (p. 725). Pearson Education. Kindle Edition. 
