import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from variable import Token, Attack, Boost

wlasciwosci = {
    ############## wojownicy
    "mutek": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 6,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS: {
            Attack.MELEE: [[0, 1], [1, 1], [5, 1]],
        },
        Token.Stats.INITIATIVE: [2]
    },
    "nożownik": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 4,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS: {
            Attack.MELEE: [[4, 1], [5, 1]],
        },
        Token.Stats.INITIATIVE: [3]
    },
    "sieciarz": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 2,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS: {
            Attack.MELEE: [[2, 3]],
        },
        Token.Stats.WIRE : [2],
        Token.Stats.INITIATIVE: [1]
    },
    "super-mutant": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 1,
        Token.Stats.HP: 2,
        Token.Stats.ATTACKS: {
            Attack.MELEE: [[0, 2], [1, 1], [5, 1]],
        },
        "pancerz" : [0, 1, 5],
        Token.Stats.INITIATIVE: [2]
    },
    "siłacz": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 2,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS: {
            Attack.MELEE: [[0, 2]],
        },
        Token.Stats.INITIATIVE: [2]
    },
    "zabojca": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 2,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS: {
            Attack.SHOOT: [[5, 1]],
        },
        "abilitki" : ["mobilność"],
        Token.Stats.INITIATIVE: [3]
    },
    ############## sztab
    "sztab": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 1,
        Token.Stats.HP: 20,
        Token.Stats.ATTACKS: {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        Token.Stats.BOOSTS: {
            Boost.INITIATIVE: [0, 1, 2, 3, 4, 5]
        },
        Token.Stats.BOOST_TARGET: "own",
        Token.Stats.INITIATIVE: [0]
    },

    ############## moduły
    "medyk": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 1,
        Token.Stats.HP: 1,
        Token.Stats.BOOSTS: {
            Boost.HEAL: [0, 1, 5]
        },
        Token.Stats.BOOST_TARGET: "own"
    },
    "oficer": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 2,
        Token.Stats.HP: 1,
        Token.Stats.BOOSTS: {
            Boost.MELEE: [0, 1, 5]
        },
        Token.Stats.BOOST_TARGET: "own"
    },
    "super-oficer": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 1,
        Token.Stats.HP: 2,
        Token.Stats.BOOSTS: {
            Boost.MELEE: [0, 1, 5]
        },
        Token.Stats.BOOST_TARGET: "own"
    },
    "zwiadowca": {
        Token.TYPE: Token.Type.BOARD,
        Token.UNIT_COUNT: 2,
        Token.Stats.HP: 1,
        Token.Stats.BOOSTS: {
            Boost.INITIATIVE: [0, 1, 5]
        },
        Token.Stats.BOOST_TARGET: "own"
    },

    ############# natychmiastowe
    Token.Type.Instant.BITWA: {
        Token.TYPE: Token.Type.INSTANT,
        Token.UNIT_COUNT: 6,
    },
    Token.Type.Instant.MOVE: {
        Token.TYPE: Token.Type.INSTANT,
        Token.UNIT_COUNT: 4,
    },
    Token.Type.Instant.GRENADE: {
        Token.TYPE: Token.Type.INSTANT,
        Token.UNIT_COUNT: 1,
    }
}