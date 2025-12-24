package com.customerregistration.consumer;

import com.customerregistration.entity.Customer;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class Consumer {
    @KafkaListener(
            topics = "customer-topic",
            groupId = "loanapp-group",
            containerFactory = "kafkaListenerContainerFactory"
    )
    public void listen(Customer customer) {
        System.out.println("Received Kafka event: " + customer);
    }
}
