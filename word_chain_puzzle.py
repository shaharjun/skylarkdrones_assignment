"""
    the following script prints the word-chain of minimum length,
    starting with one particular word and ending with another.
    Successive entries in the chain must all be real words,
    and each can differ from the previous word by just one letter.
"""
from collections import defaultdict  # default dict instead of dict for values to be auto-created when a key is missing,
import distance  # for calculating hamming distance between two words

# taking user input
ip = input("enter start and end words(seperated by space) : ").split()
begin = ip[0].lower()
end = ip[1].lower()

#  execute code only if the two strings have the same length, else print error message
if len(begin) == len(end):
    lngth = len(begin)
    word_list = []
    with open('dictionary.txt', 'r') as f:
        for line in f:
            for word in line.split():
                if len(word) == lngth:
                    word_list.append(word.lower())

    graph = defaultdict(set) # example: {'cat' : {'cot', 'cog'}, 'cot': {'cat', 'cog'} .... }


    def create_graph(graph, word_list):
        """
        :param graph: graph of words with each word as parent and its children as words which differ from parent by one place
        :param word_list: list of all n-letter words sourced from dictionary
        :return: created graph of words and their one-letter spaced children
        """
        for word1 in word_list:
            neighbours_list = []
            for word2 in word_list:
                if distance.hamming(word1, word2) == 1:
                    if word2 not in neighbours_list:
                        neighbours_list.append(word2)
            graph[word1] = set(neighbours_list)


    def bfs(graph, start_state, goal_state):
        """

        :param graph: graph of words with each word as parent and its children as words which differ from parent by one place
        :param start: start string
        :param goal: goal string
        :return: all paths from start string to goal string by performing bfs
        """
        queue = [(start_state, [start_state])]
        while queue:
            (vertex, path) = queue.pop(0)
            for next in graph[vertex] - set(path):
                if next == goal_state:
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))


    def bfs_shortest_path(graph, start, goal):
        """
        :param graph: graph of words with each word as parent and its children as words which differ from parent by one place
        :param start: start string
        :param goal: goal string
        :return: return shortest path from the paths returned by bfs
        """
        try:
            return next(bfs(graph, start, goal))
        except StopIteration:
            return None

    create_graph(graph, word_list)
    print(bfs_shortest_path(graph, begin, end))

else:
    print("The two strings must have same length")
