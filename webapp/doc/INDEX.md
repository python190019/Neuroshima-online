# Dokumentacja - Index

Punkt wejścia do aktualnej dokumentacji projektu WebSocket Neuroshima.

## Gdzie zacząć

- szybki start: `QUICKSTART.md`
- pełny opis: `doc/README.md`
- przegląd zmian: `IMPLEMENTATION_SUMMARY.md`
- główny opis repo: `README.md`

## Aktualny stan projektu

- backend: Java/Spring Boot (`pl.staszic.neu`)
- websocket: `ws://localhost:8080/ws/chat`
- protokół: `CREATENEWROOM`, `STARTNEWGAME`, `ENDTURN`, `ENDGAME` (request/response)
- klient: implementacja wyłącznie w `client/websocket_client.py`

Główny flow klienta:
1. `CREATENEWROOM_REQUEST`
2. `STARTNEWGAME_REQUEST` (`roomId`, `playerId`)
3. `ENDTURN_REQUEST` (`gameId`)
4. `ENDGAME_REQUEST` (`gameId`)

## Najważniejsze pliki

```text
webapp/
├── QUICKSTART.md
├── README.md
├── IMPLEMENTATION_SUMMARY.md
├── src/main/java/pl/staszic/neu/
│   ├── Main.java
│   ├── WebSocketConfig.java
│   ├── WebSocketHandler.java
│   ├── WebSocketController.java
│   └── messages/
│       ├── WebSocketMessage.java
│       ├── GameScopedWebSocketMessage.java
│       ├── Room.java
│       ├── CreateNewRoomRequest.java
│       ├── CreateNewRoomResponse.java
│       ├── StartNewGameRequest.java
│       ├── StartNewGameResponse.java
│       ├── EndTurnRequest.java
│       ├── EndTurnResponse.java
│       ├── EndGameRequest.java
│       └── EndGameResponse.java
├── client/
│   ├── websocket_client.py
│   ├── game_messages_example.py
│   └── test.py
└── doc/
    ├── INDEX.md
    ├── README.md
    └── prompty/
```

## Szybkie komendy

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py
```

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python test.py
```

Najczęstsze problemy:

- `ModuleNotFoundError: websocket` -> `../.venv/bin/python -m pip install -r ../requirements.txt`
- `Timeout` -> serwer jest niedostępny, sprawdź logi w `logs/websocket.log`

Szczegóły: `README.md`

---

## 📚 Dodatkowe Zasoby

- [QUICKSTART.md](../QUICKSTART.md) - 5-minutowy przewodnik
- [README.md](README.md) - Pełna dokumentacja
- [../IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) - Podsumowanie pracy
- [prompt-websocket.txt](prompty/prompt-websocket.txt) - Oryginalne wymagania

---

## 🎉 Gotowy do użytku!

```
✅ Serwer WebSocket - Java/Spring Boot
✅ Klient WebSocket - Python
✅ Komunikaty JSON
✅ Obsługa pokoi i gier (`roomId` / `gameId`)
✅ Logowanie
✅ Testowanie
✅ Dokumentacja
```

**Zacznij od:** [QUICKSTART.md](../QUICKSTART.md)

---

## 📞 Podsumowanie

Aplikacja jest gotowa do testów lokalnych i dalszej rozbudowy.

Jeśli coś nie działa:
1. Sprawdź log serwera: `logs/websocket.log`
2. Uruchom smoke test: `client/test.py`
3. Zobacz pełny opis protokołu: `doc/README.md`

