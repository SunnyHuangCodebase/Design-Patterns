from __future__ import annotations
from abc import ABC, abstractmethod


class Purchase(ABC):
  """Payment for a purchase."""
  subtotal: int
  fee: float

  def __init__(self, subtotal: int) -> None:
    self.subtotal = subtotal

  @abstractmethod
  def calculate_total(self, surcharge: Surcharge) -> int:
    """Calculates the cost based on the surcharge applied by the business."""

  def calculate_fee(self) -> int:
    return int(self.fee * self.subtotal)


class CashPurchase(Purchase):
  """Pay with cash."""
  fee: float = 0.00

  def calculate_total(self, surcharge: Surcharge):
    return self.subtotal + surcharge.add_cash_fee(self)


class DebitPurchase(Purchase):
  """Pay with debit."""
  fee: float = 0.01

  def calculate_total(self, surcharge: Surcharge):
    return self.subtotal + surcharge.add_debit_fee(self)


class GiftCardPurchase(Purchase):
  """Pay with gift card."""
  fee: float = 0.02

  def calculate_total(self, surcharge: Surcharge):
    return self.subtotal + surcharge.add_gift_card_fee(self)


class MasterCardPurchase(Purchase):
  """Pay with Mastercard."""
  fee: float = 0.03

  def calculate_total(self, surcharge: Surcharge):
    return self.subtotal + surcharge.add_mastercard_fee(self)


class VisaPurchase(Purchase):
  """Pay with Visa."""
  fee: float = 0.04

  def calculate_total(self, surcharge: Surcharge):
    return self.subtotal + surcharge.add_visa_fee(self)


class AmericanExpressPurchase(Purchase):
  """Pay with American Express."""
  fee: float = 0.05

  def calculate_total(self, surcharge: Surcharge):
    return self.subtotal + surcharge.add_american_express_fee(self)


class Surcharge(ABC):
  """How a business calculates surcharges based on payment method."""

  @abstractmethod
  def add_cash_fee(self, payment: CashPurchase) -> int:
    """Applies cash fee."""

  @abstractmethod
  def add_debit_fee(self, payment: DebitPurchase) -> int:
    """Applies debit card fee."""

  @abstractmethod
  def add_gift_card_fee(self, payment: GiftCardPurchase) -> int:
    """Applies gift card fee."""

  @abstractmethod
  def add_mastercard_fee(self, payment: MasterCardPurchase) -> int:
    """Applies Mastercard credit card fee."""

  @abstractmethod
  def add_visa_fee(self, payment: VisaPurchase) -> int:
    """Applies Visa credit card fee."""

  @abstractmethod
  def add_american_express_fee(self, payment: AmericanExpressPurchase) -> int:
    """Applies American Express credit card fee."""


class EatCosts(Surcharge):
  """Business assumes the cost of payment method fees."""

  def add_cash_fee(self, payment: CashPurchase) -> int:
    return 0

  def add_debit_fee(self, payment: DebitPurchase) -> int:
    return 0

  def add_gift_card_fee(self, payment: GiftCardPurchase) -> int:
    return 0

  def add_mastercard_fee(self, payment: MasterCardPurchase) -> int:
    return 0

  def add_visa_fee(self, payment: VisaPurchase) -> int:
    return 0

  def add_american_express_fee(self, payment: AmericanExpressPurchase) -> int:
    raise Exception(
        "Sorry, we don't accept American Express because of their fees.")


class PassOnCosts(Surcharge):
  """Business passes any payment method fees onto the customer."""

  def add_mastercard_fee(self, payment: MasterCardPurchase) -> int:
    return payment.calculate_fee()

  def add_visa_fee(self, payment: VisaPurchase) -> int:
    return payment.calculate_fee()

  def add_american_express_fee(self, payment: AmericanExpressPurchase) -> int:
    return payment.calculate_fee()

  def add_cash_fee(self, payment: CashPurchase) -> int:
    return payment.calculate_fee()

  def add_gift_card_fee(self, payment: GiftCardPurchase) -> int:
    return payment.calculate_fee()

  def add_debit_fee(self, payment: DebitPurchase) -> int:
    return payment.calculate_fee()


class DiscountCosts(Surcharge):
  """Offer higher discounts for using low-fee payment methods."""

  def add_cash_fee(self, payment: CashPurchase) -> int:
    return int(payment.calculate_fee() - payment.subtotal * 0.05)

  def add_debit_fee(self, payment: DebitPurchase) -> int:
    return int(payment.calculate_fee() - payment.subtotal * 0.05)

  def add_gift_card_fee(self, payment: GiftCardPurchase) -> int:
    return int(payment.calculate_fee() - payment.subtotal * 0.05)

  def add_mastercard_fee(self, payment: MasterCardPurchase) -> int:
    return int(payment.calculate_fee() - payment.subtotal * 0.05)

  def add_visa_fee(self, payment: VisaPurchase) -> int:
    return int(payment.calculate_fee() - payment.subtotal * 0.05)

  def add_american_express_fee(self, payment: AmericanExpressPurchase) -> int:
    return int(payment.calculate_fee() - payment.subtotal * 0.05)
