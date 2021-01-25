

class queries:
    DB_USAGE_QUERY = """
    SELECT table_schema, round(sum((data_length+index_length)/1024/1024), 2) AS MB FROM information_schema.tables GROUP BY 1;
    """

    TABLE_USAGE_QUERY = """
    SELECT
    TABLE_NAME AS 'Table',
    TABLE_ROWS AS 'Rows',
    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS `Size (MB)`
    FROM
    information_schema.TABLES
    WHERE
    TABLE_SCHEMA = "{}"
    ORDER BY
    (DATA_LENGTH + INDEX_LENGTH)
    DESC;
    """

    COUNT_BY_DAY_QUERY = """
    SELECT COUNT(*), DATE(FROM_UNIXTIME(sched_dep + origin_offset)) 
    FROM big_data.FLIGHT 
    WHERE real_dep IS NOT NULL 
    GROUP BY DATE(FROM_UNIXTIME(sched_dep + origin_offset));
    """

    COUNT_BY_DAY_JP_QUERY = """
        SELECT COUNT(*), DATE(FROM_UNIXTIME(sched_dep + origin_offset)) 
        FROM big_data.FLIGHT_JP 
        WHERE real_dep IS NOT NULL 
        GROUP BY DATE(FROM_UNIXTIME(sched_dep + origin_offset));
        """

    CARS_FULL_INFO_QUERY = """
    SELECT a.vin, a.id, a.style, a.stockType, a.brand, a.model, a.trim, a.year, a.mileage, a.price, 
    b.color, b.interior_color, b.capacity, b.fuel_type, b.driver_wheel, b.seller, b.street, b.city, b.state, b.seller_rate 
    FROM big_data.{}_{} AS a INNER JOIN car_data.{}_{}_detail AS b 
    ON a.id = b.id;
    """

    CARS_FULL_INFO_VIEW_QUERY = """
    SELECT * FROM big_data.{}_{}_view;
    """

    CREATE_ALL_CARS_INFO_VIEW_QUERY = """
    CREATE VIEW big_data.{}_{}_view AS 
    SELECT a.vin, a.id, a.style, a.stockType, a.brand, a.model, a.trim, a.year, a.mileage, a.price, 
    b.color, b.interior_color, b.capacity, b.fuel_type, b.driver_wheel, b.seller, b.street, b.city, b.state, b.seller_rate 
    FROM big_data.{}_{} AS a INNER JOIN car_data.{}_{}_detail AS b 
    ON a.id = b.id;
    """

    FLIGHT_NUM_BY_AIRLINE_QUERY = """
    SELECT flight_num, origin_iata, a.city, a.country, dest_iata, b.city, b.country 
    FROM big_data.ALL_FLIGHT, flight_data.airport as a, flight_data.airport as b 
    WHERE origin_iata = a.iata and dest_iata = b.iata and airline_iata = "{}" 
    GROUP BY flight_num, origin_iata, dest_iata;
    """

    ALL_AIRPORTS_QUERY = """
    SELECT concat(origin_iata," | ", a.city) FROM 
    big_data.ALL_FLIGHT, flight_data.airport AS a 
    WHERE origin_iata = a.iata 
    GROUP BY origin_iata;
    """

    POP_DEST_BY_AIRPORT_QUERY = """
    SELECT a.city, a.country, a.name, COUNT(*), a.iata, GROUP_CONCAT(DISTINCT(airline_iata)) 
    FROM big_data.ALL_FLIGHT, flight_data.airport as a 
    WHERE origin_iata = "{}" AND a.iata = dest_iata 
    GROUP BY dest_iata ORDER BY COUNT(*) DESC limit 10;
    """

    POP_AIRLINE_BY_AIRPORT_QUERY = """
    SELECT airline_iata, a.name, COUNT(*) 
    FROM big_data.ALL_FLIGHT, flight_data.airline AS a 
    WHERE origin_iata = "{}" AND airline_icao = a.icao 
    GROUP BY airline_icao 
    ORDER BY COUNT(*) DESC LIMIT 5;
    """

    AVG_DEP_DELAY_QUERY = """
    SELECT ROUND(AVG((real_dep-sched_dep)/60),2) 
    FROM big_data.ALL_FLIGHT 
    WHERE origin_iata = "{}";
    """

    AVG_ARR_DELAY_QUERY = """
    SELECT ROUND(AVG((real_arr-sched_arr)/60),2) 
    FROM big_data.ALL_FLIGHT 
    WHERE dest_iata = "{}";
    """

    POP_AIRCRAFT_BY_AIRPORT_QUERY = """
    SELECT a.model, COUNT(*), aircraft_code 
    FROM big_data.ALL_FLIGHT, flight_data.aircraft AS a 
    WHERE origin_iata = "{}" AND (aircraft_code = a.icao OR aircraft_code = a.iata) 
    GROUP BY aircraft_code
    ORDER BY COUNT(*) DESC LIMIT 10;
    """

    ALLIANCE_QUERY = """
    SELECT league, COUNT(*) 
    FROM big_data.ALL_FLIGHT LEFT JOIN flight_data.alliance AS a 
    ON airline_iata = a.iata 
    WHERE origin_iata = "{}" 
    GROUP BY league 
    ORDER BY COUNT(*) DESC;
    """

    AIRPORT_DEST_COORDINATE_QUERY = """
    SELECT latitude, longitude, COUNT(*) 
    FROM big_data.ALL_FLIGHT, flight_data.airport AS a 
    WHERE origin_iata = "{}" AND dest_iata = a.iata 
    GROUP BY dest_iata 
    HAVING COUNT(*) > 1 
    ORDER BY COUNT(*);
    """

    COORDINATE_BY_AIRPORT_QUERY = """
    SELECT latitude, longitude 
    FROM flight_data.airport AS a 
    WHERE iata = "{}";
    """

    TIME_SERIES_AIRPORT_QUERY = """
    SELECT COUNT(*), FROM_UNIXTIME(FLOOR((sched_dep+origin_offset) DIV (15 * 60))*(15*60), "%H:%i") AS time 
    FROM big_data.ALL_FLIGHT WHERE {}_iata = "{}" 
    GROUP BY time;
    """

    AIRPORT_DELAY_COUNT_QUERY = """
    SELECT COUNT(*) FROM big_data.ALL_FLIGHT 
    WHERE origin_iata = "{}" AND (real_dep - sched_dep) <= 1200 
    UNION 
    SELECT COUNT(*) FROM big_data.ALL_FLIGHT 
    WHERE origin_iata = "{}";
    """

    AIRPORT_DELAY_ARRIVAL_COUNT_QUERY = """
    SELECT COUNT(*) FROM big_data.ALL_FLIGHT 
    WHERE dest_iata = "{}" AND (real_arr - sched_arr) <= 900 
    UNION 
    SELECT COUNT(*) FROM big_data.ALL_FLIGHT 
    WHERE dest_iata = "{}";
    """

    AIRPORT_UNIQUE_DESTINATION_QUERY = """
    SELECT dest_iata FROM big_data.ALL_FLIGHT 
    WHERE origin_iata = "{}" GROUP BY dest_iata;
    """

    AIRLINE_POP_AIRPORT_QUERY = """
    SELECT a.name, origin_iata 
    FROM big_data.ALL_FLIGHT, flight_data.airport a 
    WHERE a.iata = origin_iata AND airline_iata = "{}" 
    GROUP BY origin_iata 
    ORDER BY COUNT(*) DESC LIMIT 15;
    """