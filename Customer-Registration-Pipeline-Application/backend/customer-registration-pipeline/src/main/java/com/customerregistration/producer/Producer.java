package com.customerregistration.producer;

import com.customerregistration.entity.Customer;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class Producer {
    private final KafkaTemplate<String, Customer> kafkaTemplate;

    public Producer(KafkaTemplate<String, Customer> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendCustomerEvent(Customer customer) {
        System.out.println("### Sending to Kafka: " + customer.getCustomer_ID());
        kafkaTemplate.send("customer-topic", customer.getCustomer_ID().toString(), customer);
    }
}