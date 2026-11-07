from ..core.errors import UnknownCodeError


class Merchant:
    SELL_PRICE_PERCENT = 50

    def __init__(self, catalog, assortment):
        self._catalog = catalog
        self._assortment = tuple(assortment)

    @property
    def showcase(self):
        return tuple(self._catalog.create(code) for code in self._assortment)

    def buy(self, hero, code):
        if code not in self._assortment:
            raise UnknownCodeError("Товар", code)
        item = self._catalog.create(code)
        hero.spend_gold(item.price)
        hero.add_item(item)
        return item

    def sell_price(self, item):
        return item.price * self.SELL_PRICE_PERCENT // 100

    def sell(self, hero, item):
        price = self.sell_price(item)
        hero.remove_item(item)
        hero.add_gold(price)
        return price
