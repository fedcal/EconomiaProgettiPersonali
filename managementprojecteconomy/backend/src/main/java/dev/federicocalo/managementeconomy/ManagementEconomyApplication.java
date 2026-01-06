package dev.federicocalo.managementeconomy;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Sistema di Gestione Economica Multi-Progetto
 *
 * Gestisce i dati finanziari di tre progetti:
 * - FedericoCalo.dev (Portfolio professionale)
 * - CasaDelleMagnolie.com (Vacation rental)
 * - PlayTheEvent.com (SaaS platform)
 *
 * @author Federico Calò
 * @version 1.0.0
 */
@SpringBootApplication
public class ManagementEconomyApplication {

    public static void main(String[] args) {
        SpringApplication.run(ManagementEconomyApplication.class, args);
    }
}
