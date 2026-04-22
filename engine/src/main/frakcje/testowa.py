from main.utils.variable import TokenKey, TokenType, InstantType, TokenStats

wlasciwosci = {
    "sieciarz": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 10,
        TokenStats.HP: 1,
        TokenStats.WIRE: [0],
        },
    "dwu-sieciarz": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 10,
        TokenStats.HP: 1,
        TokenStats.WIRE: [0, 1],
    },
    InstantType.SNIPER : {
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 1,
    }
}
