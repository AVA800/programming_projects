package com.customerregistration.controller;
import com.customerregistration.entity.Customer;
import com.customerregistration.producer.Producer;
import com.customerregistration.service.Registration;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/customers")
public class CustomerController {
    private final Registration service;
    private final Producer producer;
    public CustomerController(Registration service, Producer producer){
        this.service=service;
        this.producer = producer;
    }
    @GetMapping
    public List<Customer> getAllCustomers(){
        return service.findAll();
    }

    @GetMapping("/search")
    public Customer getCustomer(@RequestParam("id") String id){
        return service.findByCustomer_ID(Long.parseLong(id));
    }

    @PostMapping("/register")
    public Customer createCustomer(@RequestBody Customer customer){
        return service.save(customer);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteCustomer(@PathVariable("id") Long id) {
        service.delete(id);
        return ResponseEntity.ok("Customer with ID " + id + " deleted successfully.");
    }
}