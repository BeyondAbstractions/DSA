from typing import Optional, Deque, Dict, List
from collections import deque

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors: List[Node] = neighbors if neighbors is not None else []



class Solution:

    def cloneGraph_bfs(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None
        else:
            mapping: Dict[int, Node] = dict()
            q: Deque[Node]  = deque()
            q.append(node)
            source = None
            while q:
                current: Node = q.popleft()
                new_current: Optional[Node] = None
                id_current = id(current)
                if id_current not in mapping:
                    source = Node(val=current.val, neighbors=None)
                    mapping[id_current] = source
                    new_current = source
                else:
                    new_current = mapping[id_current]

                for dnode in current.neighbors:
                    id_dnode = id(dnode)
                    if id_dnode not in mapping:
                        q.append(dnode)
                        new_node: Node =  Node(val=dnode.val, neighbors=None)
                        mapping[id_dnode] = new_node
                        new_current.neighbors.append(new_node)
                    else:
                        existing_new_node:Node = mapping[id_dnode]
                        new_current.neighbors.append(existing_new_node)

            return source



    def cloneGraph_dfs(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None
        else:
            mapping: Dict[int, Node] = dict()
            stack: List[Node]  = list()
            stack.append((node, iter(node.neighbors)))
            source = None

            while stack:
                current_node, current_node_iter = stack[-1]
                new_current: Optional[Node] = None
                id_current = id(current_node)
                
                if id_current not in mapping:
                    source = Node(val=current_node.val, neighbors=None)
                    mapping[id_current] = source
                    new_current = source
                else:
                    new_current = mapping[id_current]
                
                try:
                    dnode: Node = next(current_node_iter)
                    id_dnode = id(dnode)

                    if id_dnode not in mapping:
                        stack.append((dnode, iter(dnode.neighbors)))
                        new_node: Node =  Node(val=dnode.val, neighbors=None)
                        mapping[id_dnode] = new_node
                        new_current.neighbors.append(new_node)
                    else:
                        existing_new_node:Node = mapping[id_dnode]
                        new_current.neighbors.append(existing_new_node)

                except StopIteration:
                    stack.pop()
            return source

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        # return self.cloneGraph_bfs(node=node)
        return self.cloneGraph_dfs(node=node)
            
        