#include "test_support.hpp"
#include "week04.hpp"

#include <algorithm>
#include <stdexcept>
#include <vector>

using cpp_course::week04::DirectedEdge;
using cpp_course::week04::DisjointSet;
using cpp_course::week04::Graph;
using cpp_course::week04::TreeNode;
using cpp_course::week04::bfs_distances;
using cpp_course::week04::connected_components;
using cpp_course::week04::dfs_preorder;
using cpp_course::week04::level_order;
using cpp_course::week04::topological_order;
using cpp_course::week04::tree_height;

namespace {

bool respects_edges(const std::vector<std::size_t>& order,
                    const std::vector<DirectedEdge>& edges) {
  std::vector<std::size_t> position(order.size());
  for (std::size_t index = 0; index < order.size(); ++index) {
    if (order[index] >= order.size()) {
      return false;
    }
    position[order[index]] = index;
  }
  for (const auto& edge : edges) {
    if (position[edge.first] >= position[edge.second]) {
      return false;
    }
  }
  return true;
}

template <typename Function>
bool throws_out_of_range(Function&& function) {
  try {
    function();
  } catch (const std::out_of_range&) {
    return true;
  }
  return false;
}

}  // namespace

int main() {
  course_test::Suite suite;

  suite.run("tree operations use node height and left-to-right levels", [] {
    TreeNode left_left{4};
    TreeNode left{2, &left_left, nullptr};
    TreeNode right{3};
    TreeNode root{1, &left, &right};

    COURSE_CHECK(tree_height(nullptr) == 0U);
    COURSE_CHECK(tree_height(&root) == 3U);
    COURSE_CHECK(level_order(&root) ==
                 std::vector<std::vector<int>>({{1}, {2, 3}, {4}}));
  });

  suite.run("DFS discovery order and BFS distances match graph semantics", [] {
    const Graph graph{{1, 2}, {3}, {3, 4}, {4}, {}, {}};
    COURSE_CHECK(dfs_preorder(graph, 0) ==
                 std::vector<std::size_t>({0, 1, 3, 4, 2}));
    COURSE_CHECK(bfs_distances(graph, 0) ==
                 std::vector<int>({0, 1, 1, 2, 2, -1}));
  });

  suite.run("component traversal covers disconnected and isolated nodes", [] {
    const Graph graph{{1}, {0, 2}, {1}, {4}, {3}, {}};
    COURSE_CHECK(connected_components(graph) == 3U);
    COURSE_CHECK(connected_components({}) == 0U);
    COURSE_CHECK(throws_out_of_range(
        [] { (void)connected_components(Graph{{1}, {9}}); }));
  });

  suite.run("union-find merges components idempotently", [] {
    DisjointSet sets(6);
    COURSE_CHECK(sets.component_count() == 6U);
    COURSE_CHECK(sets.unite(0, 1));
    COURSE_CHECK(sets.unite(1, 2));
    COURSE_CHECK(!sets.unite(0, 2));
    COURSE_CHECK(sets.connected(0, 2));
    COURSE_CHECK(!sets.connected(0, 5));
    COURSE_CHECK(sets.component_count() == 4U);
    COURSE_CHECK(throws_out_of_range([&] { (void)sets.find(6); }));
  });

  suite.run("topological sort respects all edges and detects cycles", [] {
    const std::vector<DirectedEdge> dag{{0, 2}, {1, 2}, {1, 3}, {2, 4},
                                         {3, 4}};
    const auto order = topological_order(5, dag);
    COURSE_CHECK(order.has_value());
    COURSE_CHECK(order->size() == 5U);
    std::vector<std::size_t> sorted = *order;
    std::sort(sorted.begin(), sorted.end());
    COURSE_CHECK(sorted == std::vector<std::size_t>({0, 1, 2, 3, 4}));
    COURSE_CHECK(respects_edges(*order, dag));

    COURSE_CHECK(!topological_order(3, {{0, 1}, {1, 2}, {2, 0}}).has_value());
    COURSE_CHECK(throws_out_of_range(
        [] { (void)topological_order(2, {{0, 2}}); }));
  });

  return suite.finish();
}
