package com.customerregistration.service;

import com.customerregistration.entity.Customer;
import com.customerregistration.producer.Producer;
import com.customerregistration.repository.CustomerRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class Registration {
    private final CustomerRepository repository;
    private final Producer producer;

    public Registration(CustomerRepository repository, Producer producer){
        this.repository=repository;
        this.producer = producer;
    }
    public List<Customer> findAll(){
        return repository.findAll();
    }
    public Customer findByCustomer_ID(Long id){
        if(repository.findById(id).isPresent()) {
            return repository.findById(id).get();
        }else{return null;}
    }
    public Customer save(Customer customer){
        Customer saved = repository.save(customer);
        producer.sendCustomerEvent(saved); // publish to Kafka
        return saved;
    }
    public void delete(Long id){
        repository.deleteById(id);
    }
}