from main.utils.variable import TokenKey, TokenType, InstantType

wlasciwosci = {
    "sieciarz": {
        "typ": "plansza",
        "liczbajednostek" : 10,
        "hp": 1,
        "siec": [0]
        },
    "dwu-sieciarz": {
        "typ": "plansza",
        "liczbajednostek" : 10,
        "hp": 1,
        "siec": [0, 1]
    },
    InstantType.SNIPER : {
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 1,
    }
}