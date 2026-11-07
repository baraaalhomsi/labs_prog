class UnknownCodeError(LookupError):
    def __init__(self, what: str, code: str):
        super().__init__(f"{what} с кодом '{code}' не существует")
