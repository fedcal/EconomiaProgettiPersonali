package dev.federicocalo.managementeconomy.exception;

/**
 * Eccezione lanciata quando si tenta di creare una risorsa duplicata
 */
public class DuplicateResourceException extends RuntimeException {

    public DuplicateResourceException(String message) {
        super(message);
    }

    public DuplicateResourceException(String message, Throwable cause) {
        super(message, cause);
    }
}
