"""Объектная модель сервиса формирования списка подарков."""

from .gift import Gift
from .gift_list import GiftList
from .occasion import Occasion
from .recipient import Recipient

__all__ = ["Gift", "GiftList", "Occasion", "Recipient"]
