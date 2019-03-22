# define ClueItem and ClueModel

from scrapy.item import Item, Field


class ClueItem(Item):
    channel = Field()
    business = Field()
    url = Field()
    from_clue_id = Field()
    # TaskRequest
    req = Field()

    project = Field()
    spider = Field()
