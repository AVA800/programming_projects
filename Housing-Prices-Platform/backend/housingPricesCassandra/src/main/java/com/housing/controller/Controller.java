package com.housing.controller;

import com.housing.databaseservice.DataBaseService;
import com.housing.entity.House;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:5173")
@RestController
@RequestMapping("/houses")
public class Controller {
    private final DataBaseService service;
    public Controller(DataBaseService service){
        this.service=service;
    }

    @PostMapping
    public House addHouse(@RequestBody House house){
        return service.addHouse(house);
    }

    @GetMapping
    public List<House> getHouses(
            @RequestParam String region,
            @RequestParam String city,
            @RequestParam(required = false) String zipcode,
            @RequestParam(required = false) String houseid,
            @RequestParam(defaultValue = "100") int limit){
        return service.getHouses(region, city, zipcode, houseid,limit);
    }
}
