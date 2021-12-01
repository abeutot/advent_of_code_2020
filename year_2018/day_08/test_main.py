import itertools
from collections import defaultdict


class Tree(object):
    def __init__(self, nodes, metadatas):
        self.nodes = nodes
        self.metadatas = metadatas


    def sum_metadata(self):
        return sum(itertools.chain.from_iterable(self.metadatas.values()))

    def node_value(self, node):
        children = self.nodes[node]

        metadatas = self.metadatas[node]

        # print('node:', node, 'children:', children, 'metadatas:', metadatas)

        if not children:
            return sum(metadatas)

        valid_children_indexes = {i for i, _ in enumerate(children)}

        return sum(self.node_value(children[m - 1])
                   for m in metadatas if (m - 1) in valid_children_indexes)

    def root_value(self):
        return self.node_value(0)

    @classmethod
    def parse(cls, input_):
        raw_tree = list(map(int, input_.rstrip('\n').split()))

        nodes = defaultdict(list)
        metadatas = {}

        todo = []
        node = None

        node_name = itertools.count()

        while raw_tree:
            # print('raw:', raw_tree, 'todo:', todo)
            if todo:
                node, what, count = todo.pop()
                if what == 'm':
                    # get the metadata
                    metadatas[node] = raw_tree[:count]
                    raw_tree = raw_tree[count:]
                    continue

                if what == 'c':
                    # see if we need more nodes
                    if count == 0:
                        continue
                    todo.append((node, what, count - 1))

            new_node = next(node_name)
            nodes[new_node]  # make sure the node is created
            if node is not None:
                nodes[node].append(new_node)

            count_children, count_metadata, *raw_tree = raw_tree

            todo.append((new_node, 'm', count_metadata))
            todo.append((new_node, 'c', count_children))

        return cls({k: v for k, v in nodes.items()}, metadatas)


input_test = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
def test_parse_tree():
    t = Tree.parse(input_test)
    assert t.nodes == {
        0: [1, 2],
        1: [],
        2: [3],
        3: [],
    }
    assert t.metadatas == {
        0: [1, 1, 2],
        1: [10, 11, 12],
        2: [2],
        3: [99],
    }

def test_sum_metadata():
    assert Tree.parse(input_test).sum_metadata() == 138


def test_root_value():
    t = Tree.parse(input_test)
    assert t.node_value(3) == 99
    assert t.root_value() == 66

if __name__ == '__main__':
    tree = Tree.parse(open('input.txt').read())
    print('sum of metadata:', tree.sum_metadata())
    print('sum of root:', tree.root_value())
