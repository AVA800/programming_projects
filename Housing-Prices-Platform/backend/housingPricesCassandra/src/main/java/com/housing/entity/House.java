package com.housing.entity;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.cassandra.core.cql.PrimaryKeyType;
import org.springframework.data.cassandra.core.mapping.PrimaryKey;
import org.springframework.data.cassandra.core.mapping.PrimaryKeyClass;
import org.springframework.data.cassandra.core.mapping.PrimaryKeyColumn;
import org.springframework.data.cassandra.core.mapping.Table;

@Getter
@Setter
@Table("houses_by_region")
public class House {
    @Getter
    @Setter
    @PrimaryKeyClass
    public static class HouseKey{
        @PrimaryKeyColumn(name="region",type= PrimaryKeyType.PARTITIONED)
        private String region;

        @PrimaryKeyColumn(name="city", type=PrimaryKeyType.PARTITIONED)
        private String city;

        @PrimaryKeyColumn(name="zipcode", type=PrimaryKeyType.PARTITIONED)
        private String zipcode;

        @PrimaryKeyColumn(name="houseid", type=PrimaryKeyType.PARTITIONED)
        private String houseid;
    }
    @PrimaryKey
    private HouseKey key;

    private String housetype;
    private String salestype;
    private Integer yearbuild;
    private Double purchaseprice;
    private Integer nrooms;
    private Double sqm;
    private Double sqmprice;
    private String area;
}
