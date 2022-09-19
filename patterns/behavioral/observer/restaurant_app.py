from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Generic, TypeVar


@dataclass
class FoodBase:
  """Base food dish."""
  name: str


@dataclass
class Topping:
  """Accompaniments to a dish."""
  name: str


class Requirement(Enum):
  """Requirements for achievements."""
  ORDER_QUANTITY = auto()    # Number of items in a single order
  ORDER_TOTAL = auto()    # Cost of a single order


class Achievement(ABC):
  """Achievements that unlock points. Subscribes to achievement requirement notifications."""
  name: str
  requirement: Requirement
  threshold: int
  progress: int = field(default=0)
  complete: bool = field(default=False)

  @abstractmethod
  def update(self, quantity: int):
    """Update the achievement's requirements."""


Achievements = TypeVar("Achievements", bound=Achievement)


@dataclass
class UnlockableAchievement(Achievement):
  """Event based achievements."""
  name: str
  requirement: Requirement
  threshold: int
  complete: bool = field(default=False)

  def update(self, quantity: int):
    """Clears the achievement if the current quantity exceeds threshold."""
    if quantity >= self.threshold:
      self.complete = True


@dataclass
class CumulativeAchievement(Achievement):
  """Achievements with cumulative requirements."""
  name: str
  requirement: Requirement
  threshold: int
  complete: bool = field(default=False)
  progress: int = field(default=0)

  def update(self, quantity: int):
    """Clears the achievement once the cumulative quantity exceeds the threshold."""
    self.progress += quantity
    if self.progress >= self.threshold:
      self.complete = True


class AchievementPublisher(Generic[Achievements]):
  """Achievement Publisher"""

  incomplete: list[Achievements]
  completed: list[Achievements]
  achievement_subscribers: dict[Requirement, list[Achievements]]

  def __init__(self, achievements: list[Achievements]):
    self.incomplete = achievements
    self.completed = []
    self.achievement_subscribers = {}

    for achievement in achievements:
      self.achievement_subscribe(achievement.requirement, achievement)

  def publish_order_notification(self, order: Order):
    """Update achievement progress."""
    for achievement in self.achievement_subscribers[Requirement.ORDER_QUANTITY]:
      achievement.update(len(order))

      if achievement.complete:
        self.complete_achievement(achievement)

    for achievement in self.achievement_subscribers[Requirement.ORDER_TOTAL]:
      achievement.update(order.total)

      if achievement.complete:
        self.complete_achievement(achievement)

  def complete_achievement(self, achievement: Achievements):
    """Complete an achievement and unsubscribes it from listeners."""
    if achievement in self.incomplete:
      self.incomplete.remove(achievement)
      self.completed.append(achievement)
    self.achievement_unsubscribe(achievement.requirement, achievement)

  def achievement_subscribe(self, requirement: Requirement,
                            achievement: Achievements):
    """Add achievement listeners."""
    if requirement not in self.achievement_subscribers:
      self.achievement_subscribers[requirement] = list()

    self.achievement_subscribers[requirement].append(achievement)

  def achievement_unsubscribe(self, requirement: Requirement,
                              achievement: Achievements):
    """Remove achievement listeners."""
    self.achievement_subscribers[requirement].remove(achievement)


@dataclass
class FoodItem:
  """Dataclass representing a dish on the menu."""
  name: str
  base: FoodBase
  toppings: list[Topping]
  price: int


@dataclass
class Order:
  """A customer's requested items."""
  cart: list[FoodItem] = field(default_factory=list)

  @property
  def total(self) -> int:
    """Total price of the items in cart."""
    return sum([item.price for item in self.cart])

  def __len__(self) -> int:
    return len(self.cart)

  def add_to_cart(self, item: FoodItem):
    """Add an item to the cart."""
    self.cart.append(item)

  def remove_item(self, item: FoodItem):
    """Remove an item from the cart."""

    self.cart.remove(item)

  def clear(self):
    """Removes all items from cart"""
    self.cart.clear()


@dataclass
class FoodOrderingApp(Generic[Achievements]):
  """App to order food and keep track of a user's orders/achievements."""
  achievements: AchievementPublisher[Achievements]
  order: Order = field(default=Order())

  def order_item(self, item: FoodItem):
    """Adds item to cart."""
    self.order.add_to_cart(item)

  def complete_order(self):
    """Sends the order and clears the cart."""
    self.achievements.publish_order_notification(self.order)
    self.order.clear()
