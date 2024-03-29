CREATE TABLE graphic_cards (
    ean VARCHAR(15),
    dlss_3_0 VARCHAR(10),
    d_sub VARCHAR(10),
    display_port VARCHAR(10),
    mini_display_port VARCHAR(10),
    dvi VARCHAR(10),
    hdmi VARCHAR(10),
    usb_C VARCHAR(10),
    card_name TEXT,
    card_id VARCHAR(25) PRIMARY KEY,
    card_price FLOAT(2),
    stock INT,
    rating_count INT,
    questions INT,
    buyers INT,
    rating FLOAT(2),
    card_manufacturer TEXT,
    card_manufacturer_code VARCHAR(70),
    chipset_brand TEXT,
    chipset_type TEXT,
    clock_speed VARCHAR(11),
    clock_speed_boost_mode VARCHAR(11),
    stream_processors INT,
    rop_units INT,
    texturing_units INT,
    rt_cores INT,
    tensor_cores INT,
    connector_type VARCHAR(25),
    card_length INT,
    card_linking TEXT,
    card_resolution VARCHAR(25),
    recommended_power_supply_wattage INT,
    led_backlighting VARCHAR(25),
    ram_capacity INT,
    ram_type VARCHAR(25),
    data_bus VARCHAR(25),
    memory_clock INT,
    cooling_type VARCHAR(25),
    fans_quantity INT,
    power_ports VARCHAR(25), 
    packaging_version TEXT
);
