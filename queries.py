

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
    SELECT COUNT(*), DATE(FROM_UNIXTIME(sched_dep - origin_offset)) 
    FROM big_data.FLIGHT 
    WHERE real_dep IS NOT NULL 
    GROUP BY DATE(FROM_UNIXTIME(sched_dep - origin_offset));
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