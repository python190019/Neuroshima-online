# Dokumentacja Aplikacji WebSocket - Neuroshima

## Spis tresci
1. Przeglad
2. Architektura
3. Instalacja
4. Uruchamianie
5. Protokol komunikatow
6. Klient Python
7. Testowanie
8. Logowanie
9. Troubleshooting

---

## 1. Przeglad

Aplikacja sklada sie z:
- serwera WebSocket w Spring Boot
- klienta Python
- prostego endpointu REST do statystyk polaczen

Aktualny protokol biznesowy opiera sie o komunikaty pokoj+gra:
- `CREATENEWROOM` (request/response)
- `STARTNEWGAME` (request/response)
- `ENDTURN` (request/response)
- `ENDGAME` (request/response)

`STARTNEWGAME_REQUEST` musi zawierac `roomId` i `playerId`.
Wiadomosci `ENDTURN` i `ENDGAME` musza zawierac `gameId`.

---

## 2. Architektura

### Java backend

Kod backendu znajduje sie w pakiecie `pl.staszic.neu`.

Najwazniejsze klasy:
- `src/main/java/pl/staszic/neu/Main.java`
- `src/main/java/pl/staszic/neu/WebSocketConfig.java`
- `src/main/java/pl/staszic/neu/WebSocketHandler.java`
- `src/main/java/pl/staszic/neu/WebSocketController.java`

Hierarchia komunikatow:
- `src/main/java/pl/staszic/neu/messages/WebSocketMessage.java`
- `src/main/java/pl/staszic/neu/messages/GameScopedWebSocketMessage.java`
- `src/main/java/pl/staszic/neu/messages/StartNewGameRequest.java`
- `src/main/java/pl/staszic/neu/messages/StartNewGameResponse.java`
- `src/main/java/pl/staszic/neu/messages/EndTurnRequest.java`
- `src/main/java/pl/staszic/neu/messages/EndTurnResponse.java`
- `src/main/java/pl/staszic/neu/messages/EndGameRequest.java`
- `src/main/java/pl/staszic/neu/messages/EndGameResponse.java`

### Python client

- `client/websocket_client.py` - jedyna implementacja klienta WebSocket
- `client/test.py` - smoke test wykorzystujacy `websocket_client.py`
- `client/game_messages_example.py` - generator przykladowych payloadow JSON (bez laczenia z serwerem)

---

## 3. Instalacja

### Wymagania
- Java 17+
- Python 3.10+

### Python dependencies

Dla Linuxa (PEP 668) zalecane jest virtualenv:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

---

## 4. Uruchamianie

### Start serwera

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew bootRun
```

Serwer udostepnia:
- WebSocket: `ws://localhost:8080/ws/chat`
- REST stats: `http://localhost:8080/api/websocket/stats`

### Start klienta

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py
```

Przyklad z parametrami:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py --server ws://localhost:8080/ws/chat --player "Anna" --room room-1 --scenario "Moloch" --turn 1 --reason "Victory points"
```

---

## 5. Protokol komunikatow

Wspolne pola (baza):
- `messageType`
- `timestamp`
- `clientId`

Wiadomosci game-scoped dodatkowo maja:
- `gameId`

### 5.1 CREATENEWROOM_REQUEST (client -> server)

```json
{
  "messageType": "CREATENEWROOM_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerName": "Anna"
}
```

### 5.2 CONNECTION (server -> client)

```json
{
  "messageType": "CONNECTION",
  "timestamp": "2026-03-25T17:05:38.833822698",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "message": "Connected"
}
```

### 5.3 CREATENEWROOM_RESPONSE (server -> client)

```json
{
  "messageType": "CREATENEWROOM_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.860000000",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "createdRoomId": "room-1",
  "serverStatus": "STARTED room=room-1 player=Anna"
}
```

### 5.4 STARTNEWGAME_REQUEST (client -> server)

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

### 5.5 STARTNEWGAME_RESPONSE (server -> client)

```json
{
  "messageType": "STARTNEWGAME_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.865660438",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "roomId": "room-1",
  "playerId": "Anna",
  "createdGameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "serverStatus": "STARTED room=room-1 game=8ef7dcb4-db11-4ddb-a8fc-2440391462bf player=Anna"
}
```

### 5.6 ENDTURN_REQUEST (client -> server)

```json
{
  "messageType": "ENDTURN_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "playerId": "Anna",
  "turnNumber": 1
}
```

### 5.7 ENDTURN_RESPONSE (server -> client)

```json
{
  "messageType": "ENDTURN_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.870845967",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "accepted": true,
  "nextPlayerId": "Anna_next"
}
```

### 5.8 ENDGAME_REQUEST (client -> server)

```json
{
  "messageType": "ENDGAME_REQUEST",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "winnerId": "Anna",
  "reason": "Victory points"
}
```

### 5.9 ENDGAME_RESPONSE (server -> client)

```json
{
  "messageType": "ENDGAME_RESPONSE",
  "timestamp": "2026-03-25T17:05:38.872774487",
  "clientId": "58a84c5a-ca0e-4a8d-bf04-11ae1152bdf4",
  "gameId": "8ef7dcb4-db11-4ddb-a8fc-2440391462bf",
  "ended": true,
  "summary": "Game ended. Winner=Anna, reason=Victory points"
}
```

---

## 6. Klient Python

Implementacja klienta WebSocket znajduje sie tylko w `client/websocket_client.py`.

Parametry `client/websocket_client.py`:
- `--server` (domyslnie: `ws://localhost:8080/ws/chat`)
- `--player` (domyslnie: `Anna`)
- `--room` (domyslnie: `room-1`)
- `--scenario` (domyslnie: `Moloch`)
- `--turn` (domyslnie: `1`)
- `--reason` (domyslnie: `Victory points`)

Przyklad:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python websocket_client.py --player "Bot-1" --room room-2 --scenario "Moloch" --turn 2 --reason "Smoke"
```

---

## 7. Testowanie

### Smoke test protokolu

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python test.py
```

### Przyklad klas komunikatow

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp/client
../.venv/bin/python game_messages_example.py
```

Skrypt wypisuje przykladowe payloady JSON i nie nawiazuje polaczenia WebSocket.

### Build Java

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
./gradlew test
```

---

## 8. Logowanie

- konfiguracja: `src/main/resources/logback.xml`
- log serwera: `logs/websocket.log`
- logger aplikacji: `pl.staszic.neu`

Podglad logow:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
tail -f logs/websocket.log
```

---

## 9. Troubleshooting

### Problem: `ModuleNotFoundError: websocket`

Zainstaluj zaleznosci w virtualenv:

```bash
cd /home/dawid/cpp/projekty/Neuroshima/webapp
.venv/bin/python -m pip install -r requirements.txt
```

### Problem: brak polaczenia z serwerem

1. uruchom backend (`./gradlew bootRun`)
2. sprawdz endpoint statystyk:

```bash
curl http://localhost:8080/api/websocket/stats
```

### Problem: zajety port 8080

Zmien port w konfiguracji Spring (`server.port`) lub zatrzymaj proces, ktory go uzywa.

---

Dokumentacja jest zgodna z aktualnym stanem kodu na 2026-03-28.
