#!/usr/bin/env python3
"""Smoke test uruchamiajacy glowny klient z parametrami testowymi."""

from websocket_client import (
    CreateNewRoomRequest,
    EndGameRequest,
    EndTurnRequest,
    StartNewGameRequest,
    WebSocketGameClient,
)


def main() -> None:
    client = WebSocketGameClient("ws://localhost:8080/ws/chat")
    client.connect()

    player = "Tester"
    room = "room-test"

    client.send(CreateNewRoomRequest(room_id=room, player_name=player))
    start_response = client.send(StartNewGameRequest(room_id=room, player_id=player, scenario="Moloch"))

    game_id = start_response.get("createdGameId")
    if not game_id:
        raise RuntimeError("Brak createdGameId")

    client.send(EndTurnRequest(game_id=game_id, player_id=player, turn_number=1))
    client.send(EndGameRequest(game_id=game_id, winner_id=player, reason="Test finished"))
    client.close()


if __name__ == "__main__":
    main()
