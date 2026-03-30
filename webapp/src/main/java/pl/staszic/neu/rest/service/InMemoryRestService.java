package pl.staszic.neu.rest.service;

import com.fasterxml.jackson.databind.JsonNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
public class InMemoryRestService implements RestService {
    private static final Logger logger = LoggerFactory.getLogger(InMemoryRestService.class);

    private final RestTemplate restTemplate;

    @Autowired
    public InMemoryRestService(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder.build();
    }

    @Override
    public JsonNode postJson(String url, JsonNode requestBody) {
        if (url == null || url.isBlank()) {
            throw new IllegalArgumentException("URL nie może być pusty");
        }
        if (requestBody == null || requestBody.isNull()) {
            throw new IllegalArgumentException("Request body nie może być pusty");
        }

        try {
            logger.info("Wysyłam POST request na: {}", url);
            JsonNode response = restTemplate.postForObject(
                url,
                requestBody,
                JsonNode.class
            );

            if (response == null || response.isNull()) {
                logger.warn("Odpowiedź z {} jest pusta", url);
                throw new RuntimeException("Serwer zwrócił pustą odpowiedź");
            }

            logger.info("Otrzymano odpowiedź z: {}", url);
            return response;

        } catch (RestClientException e) {
            logger.error("Błąd podczas POST request do {}: {}", url, e.getMessage());
            throw new RuntimeException("Nie udało się wysłać żądania POST do: " + url, e);
        }
    }
}
