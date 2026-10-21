"""全片角色表。"""
from .people import Group, Person

JORJI = Person(skin="tan", face="round", hair="curly", beard="mustache", hat="flatcap", hat_color=(70, 62, 56),
               top="jacket", top_color=(96, 70, 58), inner=(170, 160, 140), expr="grin")
JORJI_SUIT = JORJI.but(top="suit", top_color=(52, 56, 70), tie=(150, 40, 36))

GRANDPA = Person(skin="mid", face="long", hair="bald", hair_color=(160, 156, 150), beard="stubble",
                 beard_color=(150, 140, 130), top="cardigan", top_color=(120, 96, 70), inner=(200, 196, 186))
HK_GUY = Person(skin="light", face="oval", hair="side", eyes="glasses", top="hoodie", top_color=(90, 96, 104),
                expr="smile")
JOHN = Person(skin="mid", hair="short", eyes="sunglasses", hat="cap", hat_color=(150, 48, 42), hat_text="USA",
              top="flag", expr="smile")
BROWN = Person(skin="light", face="square", hair="side", hair_color=(60, 46, 40), eyes="rimless",
               top="shirt_tie", top_color=(206, 204, 196), tie=(60, 70, 110), expr="smile")
EMILY = Person(skin="light", face="oval", hair="bun", hair_color=(56, 42, 36), top="jacket",
               top_color=(70, 96, 96), inner=(212, 200, 190))
TOM = Person(skin="tan", face="square", hair="short", hair_color=(80, 60, 44), hat="cowboy",
             hat_color=(150, 108, 70), top="plaid", top_color=(150, 60, 50), expr="grin")
ALEX = Person(skin="mid", face="oval", hair="buzz", top="hoodie", top_color=(130, 62, 56))
CARPOOL = Group([
    Person(skin="light", hair="short", top="tee", top_color=(80, 90, 120)),
    Person(skin="mid", hair="long", hair_color=(60, 40, 30), top="tee", top_color=(140, 80, 90)),
    Person(skin="tan", hair="buzz", top="tee", top_color=(90, 110, 80)),
    Person(skin="mid", hair="side", eyes="glasses", top="hoodie", top_color=(110, 100, 90)),
    Person(skin="light", hair="bun", top="jacket", top_color=(100, 80, 70)),
    Person(skin="deep", hair="curly", top="polo", top_color=(70, 100, 130)),
])
CAT_GIRL = Person(skin="light", face="oval", hair="long", hair_color=(40, 32, 30), acc="catears",
                  top="tee", top_color=(196, 150, 160), expr="smile")
V50 = Person(skin="mid", face="round", hair="buzz", top="tee", top_color=(160, 52, 44), expr="grin")
SLANG = [
    Person(skin="light", hair="long", hair_color=(96, 64, 44), top="tee", top_color=(200, 180, 120), expr="talk"),
    Person(skin="tan", hair="side", acc="headphones", top="hoodie", top_color=(60, 60, 70), expr="talk"),
    Person(skin="mid", hair="bun", eyes="glasses", top="cardigan", top_color=(160, 120, 140), expr="talk"),
    Person(skin="light", face="long", hair="short", eyes="glasses", eyebags=True, top="shirt_tie",
           top_color=(196, 196, 190), tie=(90, 90, 100), expr="sad"),
]
HOOD = Person(skin="mid", hair="none", hat="hood", hat_color=(52, 52, 58), top="hoodie", top_color=(52, 52, 58),
              mystery=True)
REBEL1 = Person(skin="light", face="oval", hair="side", eyes="glasses", hat="hood", hat_color=(42, 54, 68),
                top="hoodie", top_color=(42, 54, 68), expr="nervous")
REBEL2 = Person(skin="tan", face="square", hair="short", eyes="sunglasses", hat="cap", hat_color=(48, 66, 52),
                top="jacket", top_color=(58, 76, 62), inner=(190, 186, 174), expr="nervous")
SG_MAN = Person(skin="light", face="long", hair="slick", hair_color=(30, 26, 24), top="suit",
                top_color=(40, 46, 64), tie=(140, 40, 40), expr="smile")
RELAY = Person(skin="mid", face="square", hair="slick", hair_color=(24, 22, 22), eyes="sunglasses",
               top="suit", top_color=(30, 30, 34), tie=(24, 24, 26))
MIKE = Person(skin="light", face="square", hair="short", hair_color=(206, 176, 104), top="polo",
              top_color=(70, 110, 150), expr="smile")
GRANDMA = Person(skin="mid", face="round", hair="bun", hair_color=(176, 172, 166), eyes="glasses",
                 top="cardigan", top_color=(150, 110, 120), inner=(220, 214, 204), expr="smile")
GUARD = Person(skin="tan", face="square", hair="short", hat="helmet", hat_color=(86, 92, 66),
               top="uniform", top_color=(86, 92, 66), expr="angry")
GUARD2 = GUARD.but(skin="light", face="long")
AUTHOR = Person(skin="mid", hair="short", hat="hood", hat_color=(60, 60, 64), top="hoodie",
                top_color=(60, 60, 64), shadow=True)
CLONE = Person(skin="mid", hair="short", top="jacket", top_color=(100, 100, 100))
