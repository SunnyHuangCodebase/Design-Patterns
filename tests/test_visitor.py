import pytest

from patterns.behavioral.visitor.payment_processor_fees import AmericanExpressPurchase, CashPurchase, DebitPurchase, DiscountCosts, EatCosts, GiftCardPurchase, MasterCardPurchase, PassOnCosts, Purchase, VisaPurchase


class TestVisitor:

  @pytest.fixture
  def purchases(self) -> list[Purchase]:
    return [
        CashPurchase(100),
        DebitPurchase(100),
        GiftCardPurchase(100),
        MasterCardPurchase(100),
        VisaPurchase(100),
        AmericanExpressPurchase(100),
    ]

  def test_eat_costs(self, purchases: list[Purchase]):
    surcharge = EatCosts()
    cash, debit, gift_card, mastercard, visa, american_express = purchases
    assert cash.calculate_total(surcharge) == 100
    assert debit.calculate_total(surcharge) == 100
    assert gift_card.calculate_total(surcharge) == 100
    assert mastercard.calculate_total(surcharge) == 100
    assert visa.calculate_total(surcharge) == 100

    with pytest.raises(Exception):
      assert american_express.calculate_total(surcharge) == 105

  def test_pass_on_costs(self, purchases: list[Purchase]):
    surcharge = PassOnCosts()
    cash, debit, gift_card, mastercard, visa, american_express = purchases
    assert cash.calculate_total(surcharge) == 100
    assert debit.calculate_total(surcharge) == 101
    assert gift_card.calculate_total(surcharge) == 102
    assert mastercard.calculate_total(surcharge) == 103
    assert visa.calculate_total(surcharge) == 104
    assert american_express.calculate_total(surcharge) == 105

  def test_discount_costs(self, purchases: list[Purchase]):
    surcharge = DiscountCosts()
    cash, debit, gift_card, mastercard, visa, american_express = purchases
    assert cash.calculate_total(surcharge) == 95
    assert debit.calculate_total(surcharge) == 96
    assert gift_card.calculate_total(surcharge) == 97
    assert mastercard.calculate_total(surcharge) == 98
    assert visa.calculate_total(surcharge) == 99
    assert american_express.calculate_total(surcharge) == 100


if __name__ == "__main__":
  pytest.main([__file__])
