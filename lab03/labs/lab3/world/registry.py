from ..core.errors import UnknownCodeError


class LocationRegistry:
    def __init__(self, locations):
        self._locations = {}
        for location in locations:
            if location.code in self._locations:
                raise ValueError(f"Локация '{location.code}' уже зарегистрирована")
            self._locations[location.code] = location

    def get(self, code):
        try:
            return self._locations[code]
        except KeyError:
            raise UnknownCodeError("Локация", code) from None

    def get_all(self):
        return tuple(self._locations.values())
