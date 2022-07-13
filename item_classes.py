from tileset import tile_set


class ItemObject:
    pass


class Key(ItemObject):
    id = 1
    name = 'Key'
    name_a = 'a key'
    description = 'A small rusted key. Used for opening doors.'
    tile_char = tile_set['key']['custom_tile']


class Diamond(ItemObject):
    id = 2
    name = 'Diamond'
    name_a = 'a diamond'
    description = 'A beautiful diamond. It shines brightly in the dark.'
    tile_char = tile_set["diamond"]["custom_tile"]


class Ace(ItemObject):
    id = 3
    name = 'Ace of Spades'
    name_a = 'an ace of spades'
    description = 'A worn ace of spades playing card. It has a ripped corner.'
    tile_char = '♠'

# TODO: implement IDs to distinguish different items
