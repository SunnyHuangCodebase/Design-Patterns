import pytest
from patterns.behavioral.iterator.tree_traversal import Tree


class TestIterator:

  @pytest.fixture
  def tree(self):
    tree = Tree(8)
    for num in [4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]:
      tree.add_node(num)
    return tree

  @pytest.fixture
  def unbalanced_tree(self):
    tree = Tree(1)
    for num in range(2, 16):
      tree.add_node(num)
    return tree

  def test_preorder_dfs(self, tree: Tree):
    """Test Preorder Depth First Search Traversal."""
    dfs_traversal = [node.value for node in tree.preorder_dfs()]
    assert dfs_traversal == [1, 3, 2, 5, 7, 6, 4, 9, 11, 10, 13, 15, 14, 12, 8]

  def test_bfs(self, tree: Tree):
    """Test Breadth First Search Traversal."""
    bfs_traversal = [node.value for node in tree.bfs()]
    assert bfs_traversal == [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]

  def test_unbalanced_preorder_dfs(self, unbalanced_tree: Tree):
    """Test Preorder Depth First Search Traversal."""
    dfs_traversal = [node.value for node in unbalanced_tree.preorder_dfs()]
    assert dfs_traversal == [num for num in range(15, 0, -1)]

  def test_unbalanced_bfs(self, unbalanced_tree: Tree):
    """Test Breadth First Search Traversal."""
    bfs_traversal = [node.value for node in unbalanced_tree.bfs()]
    assert bfs_traversal == [num for num in range(1, 16)]


if __name__ == "__main__":
  pytest.main([__file__])
