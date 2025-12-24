package com.housing.repository;

import com.housing.entity.House;
import org.springframework.data.cassandra.repository.CassandraRepository;

import java.util.List;

public interface HouseRepository extends CassandraRepository<House, House.HouseKey> {
    List<House> findByKeyRegionAndKeyCity(String region, String city);
    List<House> findByKeyRegionAndKeyCityAndKeyZipcode(String region, String city, String zipcode);
    List<House> findByKeyRegionAndKeyCityAndKeyZipcodeAndKeyHouseid(String region, String city, String zipcode, String houseid);
}