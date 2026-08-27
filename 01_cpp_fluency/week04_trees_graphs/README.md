# Week 4: Trees, graph traversal, union-find, and topology

## Choose the question before the algorithm

- Tree recursion: solve the same smaller question for each child.
- BFS: shortest number of edges in an unweighted graph; queue by layers.
- DFS: reachability, components, cycles, or finish order; recursion or a stack.
- Union-find: repeated merge/connectivity questions; representatives summarize
  components.
- Topological sort: dependency ordering in a DAG; a cycle means no complete
  ordering exists.

Graphs in this module use zero-based node IDs and adjacency lists. A traversal
must mark a node discovered when it is scheduled, not after all its neighbors
have already scheduled it again.

## Week plan

| Day | Work |
|---|---|
| Mon | tree height and level-order traversal |
| Tue | iterative DFS and BFS distance map |
| Wed | connected components and union-find with path compression/rank or size |
| Thu | Kahn or finish-time topological sort, including cycle detection |
| Fri | redraw traversals, run tests, update log |
| Sat | problem pack and the graph-format integration task |

## Phase exit rehearsal

On Saturday, close the starter files. From a blank file implement:

1. BFS distances on an adjacency list;
2. a union-find with `find`, `unite`, and `connected`;
3. a tiny test graph with a disconnected node.

You pass the gate only if it compiles with warnings and your explanation covers
time and space, including why path compression changes repeated-find cost.

