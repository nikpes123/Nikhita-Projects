"""
Name: Nikhita Peswani
Student ID: 31361552
"""


# ---------------------------------------TASK 1-----------------------------------------------------------
class Graph:
    def __init__(self, connections, maxIn, maxOut, origin, targets):
        """
        In my attempt, using the technique of a bipartite graph, I have created a matrix of D rows and D columns,
        this matrix would store the minimum value of the throughput(connection[2]) and the amount of
        outgoing data from i (maxOut[i]).
        I have also created two additional vertices for the network to have one single source and one sink.
        The source is at the len(maxIn) position and has an edge to the origin with data amount of maxOut[origin].
        The sink is at (len(maxIn)+1) position and has an edge to each of the targets with data amount of
        maxOut[t].
        :param connections: a list of tuples (a, b, c) where a is the ID of the data centre from which the
                            communication channel departs, b is the ID of the data centre to which the
                            communication channel arrives and c is a positive integer representing the maximum
                            throughput of that channel.
        :param maxIn: is a list of integers in which maxIn[i] specifies the maximum amount of incoming data that
                        data centre i can process per second
        :param maxOut: is a list of integers in which maxOut[i] specifies the maximum amount of outgoing data that
                        data centre i can process per second.
        :param origin: is an integer ID ∈ {0, 1, . . . , |D| − 1} of the data centre where the data to be backed up
                        is located
        :param targets: is a list of integers such that each integer i in it is such that i ∈ {0, 1, . . . , |D| − 1}
                        and indicates that backing up data to server i is fine
        Time Complexity: O(D) + O(D^2) + O(C) + O(len(targets)) = O(D^2), this complexity arises due to creation
                        of a matrix
        Space Complexity: O(D^2) where D is the number of data centres, this space is used to store the matrix
        """
        # initialising the source and the single sink
        self.source = len(maxIn)  # O(1)
        self.sink = len(maxIn) + 1  # O(1)

        # Since we are adding 2 additional data centres, we create a graph of size (D+2)*(D+2), each element data=0
        self.graph = [0] * (len(maxIn) + 2)  # O(D)
        for i in range(len(self.graph)):  # O(D^2)
            self.graph[i] = [0] * len(self.graph)

        # adding all connections in graph, the data stored would be minimum of maxOut[connection[1]] and connection[2]
        for connection in connections:  # O(C)
            self.graph[connection[0]][connection[1]] = self.find_min(maxOut[connection[1]], connection[2])
        # creating a connection from self.source to the origin
        self.graph[self.source][origin] = maxOut[origin]  # O(1)

        # adding connections from each of the possible targets to self.sink
        for t in targets:  # O(len(targets))
            self.graph[t][self.sink] = maxOut[t]

    def breadth_first_search(self, source, target, parent):
        """
        The purpose of this method is to find a path from the source to the target.
        :param source: an integer that denotes the starting point of the graph
        :param target: an integer that denotes the ending point of the graph
        :param parent: is a list of integers that keep track of the path
                        from the source node to each visited node.
        :return: a boolean value True represents if the target has been visited, else returns a false value
        Time Complexity: O(D + C), where D is the number of data centres in the graph and C is the number of connections.
                        We traverse though each vertex and edge once.
        Space Complexity: O(D) where D is the number of data centres in the graph
        """
        visited = [False] * len(self.graph)
        queue = [source]
        visited[source] = True
        while queue:
            u = queue.pop(0)
            for v in range(len(self.graph[u])):
                if visited[v] is False and self.graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == target:
                        break
        return visited[target]

    def ford_fulkerson_alg(self):
        """
        This method uses breadth first search to find the maximum flow from source to sink.
        If a path exists, it updates the residual graph.
        Time Complexity: O(C)+ O(D + C)*(O(C) + O(C))
                        =O(C) + O(D * C^2) + O(D * C^2) = O(D * C^2)
        Space : O(C)
        """
        parent_node = [-1] * (len(self.graph))  # O(C)
        maximum_flow = 0
        while self.breadth_first_search(self.source, self.sink, parent_node):  # O(D + C)
            path_flow = float("Inf")
            s = self.sink
            while s != self.source:  # O(C)
                path_flow = self.find_min(path_flow, self.graph[parent_node[s]][s])
                s = parent_node[s]
            maximum_flow += path_flow
            v = self.sink
            while v != self.source:  # O(C)
                u = parent_node[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent_node[v]
        return maximum_flow

    def find_min(self, a, b):
        """
        This is used to find the minimum of a and b. It returns 'a' if (a < b) else returns 'b'
        """
        if a < b:
            return a
        else:
            return b


def maxThroughput(connections, maxIn, maxOut, origin, targets):
    """
    The purpose of this method is to initialise a network for a system administrator responsible
    for processing the backups of a company and the data needs to be backed up in different data centres.
    This network is used to determine the maximum possible data throughput from the data centre origin
    to the data centres specified in targets, keeping in mind that each data centre has overall limits on
    the amount of incoming data it can receive per second, and also on the amount of outgoing data it can
    send per second. In my approach I have created a graph, that stores the data flow that each of the
    data centre can take in a 2x2 matrix. Then, I have used the ford fulkerson, to get the maximum possible
    flow ie throughput.
    :param connections: a list of tuples (a, b, c) where a is the ID of the data centre from which the
                            communication channel departs, b is the ID of the data centre to which the
                            communication channel arrives and c is a positive integer representing the maximum
                            throughput of that channel.
    :param maxIn: is a list of integers in which maxIn[i] specifies the maximum amount of incoming data that
                        data centre i can process per second
    :param maxOut: is a list of integers in which maxOut[i] specifies the maximum amount of outgoing data that
                        data centre i can process per second.
    :param origin: is an integer ID ∈ {0, 1, . . . , |D| − 1} of the data centre where the data to be backed up
                        is located
    :param targets: is a list of integers such that each integer i in it is such that i ∈ {0, 1, . . . , |D| − 1}
                        and indicates that backing up data to server i is fine
    Time Complexity: O(D^2) + O(D * C^2) = O(D * C^2)
    Space Complexity: O(D^2) + O(C) = O(D^2)
    """
    g = Graph(connections, maxIn, maxOut, origin, targets)
    return g.ford_fulkerson_alg()


# ---------------------------------------TASK 2-----------------------------------------------------------
class TrieNode:
    def __init__(self, char=None):
        """
        The purpose of this method is to initialise the nodes of the CatsTrie. It takes as input the char
        that represents this node. Each node stores attributes such as:
        value : unique character in a sentence
        children = the characters that  connect to the value
        is_end = denotes if this node is the last word of the sentence
        count = the number of times this node has been used.
        Time Complexity : O(1)
        Space Complexity : O(1)
        """
        self.value = char
        self.children = [None] * 26  # Updated to 26 as there are 26 lowercase letters
        self.is_end = False
        self.count = 0


class CatsTrie:
    def __init__(self, sentences):
        """
        The purpose of this method is to initialise a CatsTrie. This method takes in a list of sentences.
        We initialise the root as an empty node and insert all the sentences one by one.
        Time Complexity: O(NM) where N is the number of sentences in the input list and M is the length
                        of the longest sentence.
        Space Complexity: O(1)
        """
        self.root = TrieNode()
        for sentence in sentences:
            self.insert_sentence(sentence)

    def insert_sentence(self, sentence):
        """
        The purpose of this method is to insert a given sentence into the trie. We start from the children
        of the root to see if the ord() of each char exists or not. whichever char does not exist, we
        add it to the children of the current node.
        Time Complexity: O(M) where M is the size of the sentence
        Space Complexity: O(1)
        """
        current = self.root
        for char in sentence:
            index = ord(char) - 97  # Calculate the index based on the character's ASCII value
            if current.children[index] is not None:
                current = current.children[index]
            else:
                current.children[index] = TrieNode(char)  # Create a new Node for the character
                current = current.children[index]
        current.is_end = True
        current.count += 1

    def find_sentences_with_prompt(self, prompt):
        """
        Input: a string called prompt
        Description: The purpose of this method is to find the sentences in the trie that start with
                    the given prompt. We start with traversing each of the char in the prompt, if the
                    prompt is not found in the trie, we return a empty list. Else we
        Output: a list of tuples such that tuple[0] represents the sentence and tuple[1] represents
                count of this sentence in the trie.
        Time Complexity:  O(X + Y )
        Space = O(k), where k is the number of sentences starting with prompt
        """
        # O(X), length of the prompt
        current = self.root
        for char in prompt:
            index = ord(char) - 97
            if current.children[index] is None:
                return []
            current = current.children[index]
        words = []
        stack = [(current, prompt)]

        # O(Y), number of nodes in the trie (ie length of the most frequent sentence in sentences
        # that begins with the prompt )
        while stack:
            node, word = stack.pop()
            if node.is_end:
                words.append((word, node.count))
            for child in node.children:
                if child is not None:
                    stack.append((child, word + child.value))
        return words

    def autoComplete(self, prompt):
        """
        Input: a string called prompt
        Description: This method aims to find the return a string that represents the completed
                    sentence from the prompt. If such a sentence exists, it returns the sentence
                    with the highest frequency. If the multiple sentences exist that start with
                    the prompt,the string that is lexicographically smaller would be returned.
                    If a string does not exist, we return None.
        Output: a string that auto completes the prompt, given it starts with the prompt
        Time Complexity: O(X + Y )
        Space = O(k), where k is the number of sentences starting with prompt
        """
        # I first find all the sentences starting with the prompt in a list
        words = self.find_sentences_with_prompt(prompt)
        # if no sentences exists I return None
        if len(words) == 0:
            return None
        # If one sentence exists, I return that sentence
        if len(words) == 1:
            return words[0][0]
        # if more than one sentence exists, I find the one with the highest frequency
        order = 0
        for i in range(1, len(words)):
            if words[i][1] > words[order][1]:
                order = i
        # Then I check if sentences with similar frequency exists
        max_list = []
        for i in range(0, len(words)):
            if words[i][1] == words[order][1]:
                max_list.append(words[i])
        #  if no other items exists with the similar frequency, I return this sentence
        if len(max_list) == 1:
            return max_list[0][0]
        # Else I find the sentence that is lexicographically smaller
        index = 0
        for i in range(1, len(max_list)):
            if max_list[i][0] < max_list[index][0]:
                index = i
        return max_list[index][0]
