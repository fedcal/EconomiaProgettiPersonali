package dev.federicocalo.managementeconomy.exception;

/**
 * Eccezione lanciata quando i dati forniti non sono validi
 */
public class InvalidDataException extends RuntimeException {

    public InvalidDataException(String message) {
        super(message);
    }

    public InvalidDataException(String message, Throwable cause) {
        super(message, cause);
    }
}
