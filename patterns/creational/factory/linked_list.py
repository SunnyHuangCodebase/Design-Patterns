from __future__ import annotations
from abc import ABC
from enum import Enum
from typing import Any


class Node(ABC):
  """Linked list node containing a value and reference to the next node."""
  value: Any | None
  next: Node | None

  def __init__(self, value: Any | None = None, next: Node | None = None):
    self.value = value
    self.next = next

  def __str__(self):
    return f"Node({self.value})"


class IntNode(Node):
  """Node with int values."""
  value: int
  next: IntNode


class StrNode(Node):
  """Node with string values."""
  value: str
  next: StrNode


class Nodes(Enum):
  "Enumerated Node types to streamline factory creation of Nodes."
  STR = StrNode
  INT = IntNode

  def __call__(self, *args: Any, **kwargs: Any):
    return self.value(*args, **kwargs)


class MixedLinkedListType(Exception):
  """New Node value is not of the same type as existing Nodes."""

  def __str__(self):
    return f"Node value does not match linked list values."


class LinkedList:
  """LinkedList Node Factory Method."""
  head: Node
  current: Node

  def __str__(self):
    head = self.head
    node_list: list[str] = [f"{head}"]
    while head.next:
      node_list.append(f"{head.next}")
      head = head.next

    return ", ".join(node_list)

  def __init__(self, value: Any):
    self.head = self.current = self.create_node(value)
    print(self.head)

  def create_node(self, value: Any):
    """Factory method to create a node"""
    if getattr(self, "current", None) and type(value) != type(
        self.current.value):
      raise MixedLinkedListType
    data_type = type(value).__name__.upper()
    node = getattr(Nodes, data_type)
    return node(value)

  def next(self, value: Any | None = None):
    """Get next node. If none, and value supplied, create node with supplied value."""

    if not self.current.next and not value:
      return

    if not self.current.next:
      try:
        self.current.next = self.create_node(value)
      except MixedLinkedListType:
        print(
            f"Unable to add {type(value)} Node to {type(self.current.value)} LinkedList."
        )
        raise

    self.current = self.current.next
    print("Next:", self.current)

  def reset(self):
    """Reset the linked list to the start of the list"""
    self.current = self.head
    self._next = self.current.next
    print("Reset:", self.current)


if __name__ == "__main__":
  linked_list = LinkedList(1)
  linked_list.next(2)
  linked_list.next(3)
  linked_list.reset()
  linked_list.next(5)
  linked_list.next()
  linked_list.next()
  linked_list.next()
