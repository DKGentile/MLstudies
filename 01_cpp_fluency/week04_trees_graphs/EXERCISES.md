# Week 4 exercises

## A. Contract implementation

Implement every `TODO` in `starter/week04.cpp`. Iterative DFS must visit
neighbors in the order stored in the adjacency list; account for stack reversal
without changing the graph. Topological output can vary, so validate dependency
positions instead of expecting one memorized ordering.

Add tests for a skewed tree, a self-loop, duplicate undirected edges, repeated
union operations, a disconnected DAG, and a directed cycle.

## B. Perception-pipeline dependency graph

Model these stages as nodes: capture, decode, resize, normalize, infer, suppress,
track, render, record. Add plausible dependency edges, produce a topological
order, then introduce one accidental back-edge and confirm cycle detection.
Write which stages could run concurrently and which share mutable state.

## C. Problem pack

Use LeetCode 104, 226, 102, 200, 207, 210, 994, 547, and 684. Complete five,
including one tree, one grid traversal, one dependency graph, and one
union-find problem. Log the selected state representation before coding.

## D. Explain-it gate

Without notes, answer: why BFS gives shortest paths only for unweighted (or
equal-weight) edges; when DFS recursion can overflow; why union by rank/size is
paired with path compression; and what an indegree of zero means.

