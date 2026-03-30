package pl.staszic.neu.rest.service;

import com.fasterxml.jackson.databind.JsonNode;

public interface RestService {

    /**
     * Wysyła POST request na podany URL z JSON-em i odbiera JSON-a
     *
     * @param url adres URL do wysłania żądania
     * @param requestBody ciało żądania (JsonNode)
     * @return odpowiedź jako JsonNode
     * @throws RuntimeException jeśli żądanie się nie powiedzie
     */
    JsonNode postJson(String url, JsonNode requestBody);

}
