package com.housing.databaseservice;

import com.housing.entity.House;
import com.housing.repository.HouseRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

@Service
public class DataBaseService {
    private final HouseRepository repo;

    public DataBaseService(HouseRepository repo) {
        this.repo = repo;
    }

    public House addHouse(House house) {
        if (house.getKey().getHouseid() == null || house.getKey().getHouseid().isBlank()) {
            String newId = String.valueOf(ThreadLocalRandom.current().nextLong(100000, 999999999));
            house.getKey().setHouseid(newId);
        }
        return repo.save(house);
    }
    public List<House> getHouses(String region, String city, String zipcode, String houseid, int limit) {
        List<House> results;
        if (zipcode != null && houseid != null) {
            results = repo.findByKeyRegionAndKeyCityAndKeyZipcodeAndKeyHouseid(region, city, zipcode, houseid);
        } else if (zipcode != null) {
            results = repo.findByKeyRegionAndKeyCityAndKeyZipcode(region, city, zipcode);
        }
        else {
            results = repo.findByKeyRegionAndKeyCity(region, city);
        }
        return results.stream().limit(limit).toList();
    }
}