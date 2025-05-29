class Potion:
    def __init__(
        self,
        name,
        description,
        targeted: bool,  # used to prompt the user to select target
    ):
        self.name = name
        self.description = description
        self.targeted = targeted
