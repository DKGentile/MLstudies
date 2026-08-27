#pragma once

#include <cstddef>
#include <optional>
#include <utility>
#include <vector>

namespace cpp_course::week04 {

struct TreeNode {
  int value;
  TreeNode* left = nullptr;
  TreeNode* right = nullptr;
};

using Graph = std::vector<std::vector<std::size_t>>;
using DirectedEdge = std::pair<std::size_t, std::size_t>;

// Height is measured in nodes: an empty tree is 0 and a leaf is 1.
std::size_t tree_height(const TreeNode* root);

// Returns values grouped by depth, left child before right child.
std::vector<std::vector<int>> level_order(const TreeNode* root);

// Returns discovery order from start. Neighbors are considered in stored order.
// Throws std::out_of_range for an invalid start or neighbor ID.
std::vector<std::size_t> dfs_preorder(const Graph& graph, std::size_t start);

// Returns unweighted edge distances from start; -1 means unreachable.
// Throws std::out_of_range for an invalid start or neighbor ID.
std::vector<int> bfs_distances(const Graph& graph, std::size_t start);

// Counts connected components of an undirected adjacency-list graph. Throws
// std::out_of_range when a neighbor ID is invalid.
std::size_t connected_components(const Graph& graph);

class DisjointSet {
 public:
  explicit DisjointSet(std::size_t element_count);

  // Element-taking operations throw std::out_of_range for an invalid ID.
  std::size_t find(std::size_t element);
  bool unite(std::size_t left, std::size_t right);
  bool connected(std::size_t left, std::size_t right);
  std::size_t component_count() const noexcept;

 private:
  std::vector<std::size_t> parent_;
  std::vector<std::size_t> rank_or_size_;
  std::size_t component_count_ = 0;
};

// Returns any valid ordering of [0, node_count), or std::nullopt if a cycle
// exists. Throws std::out_of_range when an edge endpoint is invalid.
std::optional<std::vector<std::size_t>> topological_order(
    std::size_t node_count, const std::vector<DirectedEdge>& edges);

}  // namespace cpp_course::week04
