import pytest

from patterns.behavioral.observer.restaurant_app import AchievementPublisher, Achievements, CumulativeAchievement, FoodBase, FoodItem, FoodOrderingApp, Requirement, Topping, UnlockableAchievement


class TestObserver:

  @pytest.fixture
  def menu(self):
    sandwich = FoodBase("sandwich")
    pizza = FoodBase("pizza")
    pasta = FoodBase("pasta")

    bacon = Topping("bacon")
    chicken = Topping("chicken")
    cheese = Topping("cheese")
    tomato_sauce = Topping("tomato_sauce")
    mushroom = Topping("mushroom")
    onion = Topping("onion")
    parmesan = Topping("parmesan")

    return {
        "Pasta Carbonara":
            FoodItem("Pasta Carbonara", pasta, [bacon, cheese, parmesan], 8_00),
        "Vegetarian Pizza":
            FoodItem("Vegetarian Pizza", pizza,
                     [tomato_sauce, cheese, mushroom, onion], 15_00),
        "Chicken Deluxe Sandwich":
            FoodItem("Chicken Deluxe Sandwich", sandwich,
                     [chicken, bacon, mushroom, cheese], 8_00)
    }

  @pytest.fixture
  def achievements(self):
    return [
        CumulativeAchievement("New Customer", Requirement.ORDER_QUANTITY, 1),
        CumulativeAchievement("Valued Customer", Requirement.ORDER_QUANTITY, 5),
        CumulativeAchievement("Loyal Customer", Requirement.ORDER_QUANTITY, 10),
        UnlockableAchievement("Snack", Requirement.ORDER_TOTAL, 10_00),
        UnlockableAchievement("Deluxe", Requirement.ORDER_TOTAL, 20_00),
        UnlockableAchievement("Gourmet", Requirement.ORDER_TOTAL, 30_00)
    ]

  @pytest.fixture
  def publisher(self, achievements: list[Achievements]):
    return AchievementPublisher(achievements)

  @pytest.fixture
  def app(self, publisher: AchievementPublisher[Achievements]):
    return FoodOrderingApp(publisher)

  def test_add_item(self, menu: dict[str, FoodItem],
                    app: FoodOrderingApp[Achievements]):
    for item in menu.values():
      app.order_item(item)

    total_price = app.order.total
    item_quantity = len(app.order)
    app.complete_order()
    assert total_price == 31_00
    assert UnlockableAchievement("Gourmet", Requirement.ORDER_TOTAL, 30_00,
                                 True) in app.achievements.completed
    assert CumulativeAchievement("Loyal Customer", Requirement.ORDER_QUANTITY,
                                 10, False,
                                 item_quantity) in app.achievements.incomplete

  def test_remove_item(self, menu: dict[str, FoodItem],
                       app: FoodOrderingApp[Achievements]):

    for item in menu.values():
      app.order_item(item)

    while app.order.cart:
      app.order.remove_item(app.order.cart[0])

    assert app.order.cart == []


if __name__ == "__main__":
  pytest.main([__file__])
