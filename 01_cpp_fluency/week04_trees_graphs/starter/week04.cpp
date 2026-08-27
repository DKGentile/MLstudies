#include "week04.hpp"

#include <stdexcept>

namespace cpp_course::week04 {

std::size_t tree_height(const TreeNode* root) {
  (void)root;
  throw std::logic_error("TODO: implement tree_height");
}

std::vector<std::vector<int>> level_order(const TreeNode* root) {
  (void)root;
  throw std::logic_error("TODO: implement level_order");
}

std::vector<std::size_t> dfs_preorder(const Graph& graph, std::size_t start) {
  (void)graph;
  (void)start;
  throw std::logic_error("TODO: implement dfs_preorder");
}

std::vector<int> bfs_distances(const Graph& graph, std::size_t start) {
  (void)graph;
  (void)start;
  throw std::logic_error("TODO: implement bfs_distances");
}

std::size_t connected_components(const Graph& graph) {
  (void)graph;
  throw std::logic_error("TODO: implement connected_components");
}

DisjointSet::DisjointSet(std::size_t element_count) {
  (void)element_count;
  throw std::logic_error("TODO: implement DisjointSet constructor");
}

std::size_t DisjointSet::find(std::size_t element) {
  (void)element;
  throw std::logic_error("TODO: implement DisjointSet::find");
}

bool DisjointSet::unite(std::size_t left, std::size_t right) {
  (void)left;
  (void)right;
  throw std::logic_error("TODO: implement DisjointSet::unite");
}

bool DisjointSet::connected(std::size_t left, std::size_t right) {
  (void)left;
  (void)right;
  throw std::logic_error("TODO: implement DisjointSet::connected");
}

std::size_t DisjointSet::component_count() const noexcept {
  return component_count_;
}

std::optional<std::vector<std::size_t>> topological_order(
    std::size_t node_count, const std::vector<DirectedEdge>& edges) {
  (void)node_count;
  (void)edges;
  throw std::logic_error("TODO: implement topological_order");
}

}  // namespace cpp_course::week04

