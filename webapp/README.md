# WebSocket Application - Neuroshima

Aplikacja czasu rzeczywistego oparta o Spring Boot (Java) i klienta Python.

## Spis treści

- [Szybki start](#szybki-start)
- [Aktualny protokół](#aktualny-protokol)
- [Uruchamianie](#uruchamianie)
- [Testowanie](#testowanie)
- [Struktura projektu](#struktura-projektu)
- [Dokumentacja](#dokumentacja)

---

## Szybki start

1) Uruchom backend:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

2) W osobnym terminalu uruchom klienta:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
python websocket_client.py
```

Domyślny flow klienta:
1. `CREATENEWROOM_REQUEST`
2. `STARTNEWGAME_REQUEST`
3. `ENDTURN_REQUEST`
4. `ENDGAME_REQUEST`

---

## Aktualny protokol

Backend działa w pakiecie `pl.staszic.neu` i obsługuje komunikaty JSON:

- `CREATENEWROOM_REQUEST` / `CREATENEWROOM_RESPONSE`
- `STARTNEWGAME_REQUEST` / `STARTNEWGAME_RESPONSE`
- `ENDTURN_REQUEST` / `ENDTURN_RESPONSE`
- `ENDGAME_REQUEST` / `ENDGAME_RESPONSE`

Wymagane pola:

- `STARTNEWGAME_REQUEST`: `roomId`, `playerId`
- `ENDTURN_REQUEST`: `gameId`
- `ENDGAME_REQUEST`: `gameId`

Przykład `STARTNEWGAME_REQUEST`:

```json
{
  "messageType": "STARTNEWGAME_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerId": "Anna",
  "playerName": "Anna",
  "scenario": "Moloch"
}
```

Przykład `STARTNEWGAME_RESPONSE`:

```json
{
  "messageType": "STARTNEWGAME_RESPONSE",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerId": "Anna",
  "createdGameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "serverStatus": "STARTED room=room-1 game=8ef7dcb4-db11-4ddb-a8fc-2440391462bf player=Anna"
}
```

---

## Uruchamianie

### Wymagania

- Java 17+
- Python 3.10+

### Instalacja zależności Python

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

### Serwer

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

Endpointy:

- WebSocket: `ws://localhost:8080/ws/chat`
- REST stats: `http://localhost:8080/api/websocket/stats`

### Klient (jedyna implementacja)

Jedyna implementacja klienta WebSocket jest w pliku `client/websocket_client.py`.

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py --server ws://localhost:8080/ws/chat --player "Bot-1" --room room-2 --scenario "Moloch" --turn 2 --reason "Smoke"
```

Parametry `websocket_client.py`:

- `--server` (domyślnie `ws://localhost:8080/ws/chat`)
- `--player` (domyślnie `Anna`)
- `--room` (domyślnie `room-1`)
- `--scenario` (domyślnie `Moloch`)
- `--turn` (domyślnie `1`)
- `--reason` (domyślnie `Victory points`)

---

## Testowanie

Smoke test (wykorzystuje klasy z `client/websocket_client.py`):

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python test.py
```

Generator przykładowych payloadów JSON (bez połączenia WebSocket):

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python game_messages_example.py
```

Build Java:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew test
```

---

## Struktura projektu

```text
webapp/
├── README.md
├── QUICKSTART.md
├── requirements.txt
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
    └── README.md
```

---

## Dokumentacja

- Szybki przewodnik: `QUICKSTART.md`
- Pełna dokumentacja: `doc/README.md`
- Indeks dokumentacji: `doc/INDEX.md`

---

## Rozwiązywanie problemów

- `ModuleNotFoundError: websocket`: zainstaluj zależności z `requirements.txt`
- Brak połączenia: sprawdź, czy backend działa (`./gradlew bootRun`)
- Port 8080 zajęty: zmień `server.port` lub zatrzymaj proces zajmujący port

Szczegóły w: `doc/README.md`

---

## 📚 Dokumentacja

- **[QUICKSTART.md](QUICKSTART.md)** - 5 minut do pracy
- **[doc/INDEX.md](doc/INDEX.md)** - Punkt wejścia
- **[doc/README.md](doc/README.md)** - Pełna dokumentacja
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Podsumowanie

---

## 🎓 Nauczanie

Kod jest dobrze skomentowany:

**Java:**
- `WebSocketHandler.java` - Obsługa zdarzeń WebSocket
- `WebSocketMessage.java` - Format komunikatów
- `logback.xml` - Konfiguracja logowania

**Python:**
- `websocket_client.py` - Klient sekwencyjny dla START/ENDTURN/ENDGAME
- `test.py` - Test smoke nowego protokołu

---

## 🚀 Następne kroki

1. Przeczytaj: [QUICKSTART.md](QUICKSTART.md)
2. Uruchom serwer: `./gradlew bootRun`
3. Uruchom klienta: `python websocket_client.py`
4. Czytaj dokumentację: [doc/INDEX.md](doc/INDEX.md)

---

## 📊 Statystyki

```
Java:
  - WebSocketHandler.java: obsluga request/response
  - Komunikaty: baza + klasy STARTNEWGAME/ENDTURN/ENDGAME
  - Logback.xml: 46 linii

Python:
  - websocket_client.py: klient CLI dla protokolu gry
  - test.py: prosty test end-to-end

Dokumentacja:
  - README.md
  - QUICKSTART.md
  - IMPLEMENTATION_SUMMARY.md
```

---

## ✅ Status

- ✅ Kod skompilowany bez błędów
- ✅ Serwer startuje
- ✅ Klient działa
- ✅ Testy przechodzą
- ✅ Dokumentacja kompletna
- ✅ Gotowe do produkcji

---

## 📄 Licencja

Część projektu Neuroshima - 2026

---

## 🎉 Uwagi

> "Całą aplikację można uruchomić w 5 minut bez żadnych problemów." - Instrukcja QUICKSTART

**Zacznij tutaj:** [QUICKSTART.md](QUICKSTART.md)

```bash
# W jednej linijce:
./gradlew bootRun & sleep 2 && cd client && python websocket_client.py --player "Bot-1"
```

---

**Happy WebSocketing! 🚀**

