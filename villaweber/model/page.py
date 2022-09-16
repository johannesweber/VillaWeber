class Page():

    title = None
    accordion_items = None
    cards = None

    def __init__(self) -> None:
        self.accordion_items = []
        self.cards = []
        self.title = str


class AccordionItem():

    title = None
    cards = None

    def __init__(self, title) -> None:
        self.cards = []
        self.title = title

    def add_card(self, card):
        self.cards.append(card)


class Card():
    
    title = None
    subtitle = None

    def __init__(self, title, subtitle=None) -> None:
        self.title = title
        self.subtitle = subtitle