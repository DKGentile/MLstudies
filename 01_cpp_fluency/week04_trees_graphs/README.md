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

## Prepare

Required reading, about 35-45 minutes total:

- Read Cornell CS 2110's [Trees and their Iterators](https://www.cs.cornell.edu/courses/cs2110/2025fa/lectures/lec16/)
  through subtrees, height/depth, and the recursive view of a tree. Reduce a tree
  question to work at one node plus the same question on its child subtrees.
- Read Princeton's [Undirected Graphs](https://algs4.cs.princeton.edu/41graph/)
  through graph representation, DFS, paths, and BFS. Focus on adjacency lists,
  discovery timing, and why BFS layers measure shortest paths by edge count.
- Read Princeton's [Union-Find case study](https://algs4.cs.princeton.edu/15uf/)
  through weighted quick-union and path compression. Track the representative
  invariant and how weighting limits tree height.
- Read Princeton's [Directed Graphs](https://algs4.cs.princeton.edu/42digraph/)
  sections on cycles, DAGs, and topological sort, then read the official
  [Course Schedule](https://leetcode.com/problems/course-schedule/) statement.
  State what an ordering certifies and what a directed cycle prevents before
  opening the built-in hints.
- Inspect Microsoft's [`std::queue` reference](https://learn.microsoft.com/en-us/cpp/standard-library/queue-class?view=msvc-170)
  for the FIFO operations used by a layer-ordered traversal.

Optional videos: use [MIT 6.006 Lecture 13: BFS](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-13-breadth-first-search-bfs/)
or [Lecture 14: DFS and topological sort](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-14-depth-first-search-dfs-topological-sort/)
for whichever traversal is less secure.

Before coding, verify that you can:

- state the base case and smaller subtree question for a recursive tree operation;
- choose an adjacency representation and identify the exact discovery event;
- match shortest unweighted path, reachability, repeated connectivity, and
  dependency ordering to the appropriate abstraction;
- state the representative and tree-size/rank invariants maintained by union-find;
  and
- explain what indegree zero certifies and why a remaining directed cycle blocks
  a complete topological order.

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
