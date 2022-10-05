"""The Iterator design pattern allows for multiple ways to traverse a collection.

In this case, the Tree is responsible for managing a collection of TreeNodes.
The Iterator is separate from the Tree to uphold the Single Responsibility Principle.

Each Iterator has a different method of accessing the Tree's values.
A new Iterator might be needed if the collection changes its structure
or if an alternate way to iterate over a collection is desired.

For example, it is possible to traverse a Tree with Depth or Breadth First Search.
Alternatively, the Tree can be subclassed into a Binary Search Tree or Trie.
Each case could require a new iteration algorithm to produce the desired order.
"""

from __future__ import annotations
from abc import ABC
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


class Node(ABC):
  """A node containing a value."""
  value: Any


@dataclass
class TreeNode(Node):
  """A node containing a value and up to two children."""
  value: int
  left: TreeNode | None = None
  right: TreeNode | None = None

  def __str__(self) -> str:
    return str(self.value)


Nodes = TypeVar("Nodes", bound=Node)


class Collection(ABC, Generic[Nodes]):
  """A collection of items."""
  root: Nodes


class Tree(Collection[TreeNode]):
  """A collection of tree nodes."""
  root: TreeNode

  def __init__(self, value: int = 0):
    self.root = TreeNode(value)

  def preorder_dfs(self) -> PreorderDFS:
    """Return Preorder DFS Tree Iterator."""
    return PreorderDFS(self)

  def bfs(self) -> BreadthFirstSearch:
    """Return BFS Tree Iterator."""
    return BreadthFirstSearch(self)

  def add_node(self, value: int):
    """Add nodes to tree based on value."""
    node = self.root
    while True:
      if value >= node.value:
        if not node.right:
          node.right = TreeNode(value)
          break
        else:
          node = node.right
      elif value < node.value:
        if not node.left:
          node.left = TreeNode(value)
          break
        else:
          node = node.left


class PreorderDFS(Iterator[TreeNode]):
  collection: Collection[TreeNode]
  stack: list[TreeNode]
  index: int = 0

  def __init__(self, collection: Collection[TreeNode]) -> None:
    self.collection = collection
    self.stack = []
    self.traverse(collection.root)
    print(self.collection)

  def __next__(self):
    """Returns the next tree node when performing DFS traversal of a tree."""
    try:
      node = self.stack[self.index]
      self.index += 1
    except IndexError:
      raise StopIteration

    return node

  def traverse(self, node: TreeNode):
    """Recursive traversal algorithm."""
    if node.left:
      self.traverse(node.left)
    if node.right:
      self.traverse(node.right)

    print(node)
    self.stack.append(node)


class BreadthFirstSearch(Iterator[TreeNode]):
  collection: Collection[TreeNode]
  stack: list[TreeNode]
  index: int = 0

  def __init__(self, collection: Collection[TreeNode]) -> None:
    self.collection = collection
    self.stack = []
    self.traverse(collection.root)

  def __next__(self):
    """Returns the next tree node when performing BFS traversal of a tree."""
    try:
      node = self.stack[self.index]
      self.index += 1
    except IndexError:
      raise StopIteration

    return node

  def traverse(self, node: TreeNode):
    """Recursive traversal algorithm."""
    self.stack.append(node)
    for node in self.stack:
      if node.left:
        self.stack.append(node.left)
      if node.right:
        self.stack.append(node.right)
