drop database if exists security;
create database security;
use security;

create table security_network
    (loc            varchar(30),
     network_num    varchar(8) not null,
     primary key    (network_num)
    );

create table employee
    (employee_id    varchar(8) no null,
     lname          varchar(15),
     fname          varchar(15),
     network_num    varchar(8),
     primary key    (employee_id),
     foreign key    (network_num) references security_network(network_num)
                    on delete set null
    );

create table home
    (home_name      varchar(15),
     contact        varchar(15),
     street_address varchar(40) not null,
     network_num    varchar(8),
     primary key    (street_address),
     foreign key    (network_num) references security_network(network_num)
                    on delete set null
    );

create table camera_network
    (server_IP      varchar(10),
     network_id     varchar(8) not null,
     primary key    (network_id)
    );

create table outdoor_camera
    (num            int,
     loc            varchar(25),
     IP             varchar(10) not null,
     cam_name       varchar(15),
     street_address varchar(40),
     unique         (num),
     network_id     varchar(8),
     primary key    (IP),
     foreign key    (street_address) references home(street_address)
                    on delete cascade,
     foreign key    (network_id) references camera_network(network_id)
                    on delete set null
    );

create table incident
    (instrusion_type    varchar(15),
     lost_equity        varchar(10),
     occured_time       time,
     current_day        date,
     incident_id        varchar(8) not null,
     street_address     varchar(40),
     network_id         varchar(8),
     primary key        (incident_id),
     foreign key        (street_address) references home(street_address)
                        on delete set null,
     foreign key        (network_id) references camera_network(network_id)
                        on delete set null
    );

create table security_device
    (device_type        varchar(15),
     serial_no          varchar(15) not null,
     device_IP          varchar(10) not null,
     street_address     varchar(40),
     primary key        (serial_no, device_IP),
     foreign key        (street_address) references home(street_address)
                        on delete cascade
    );

create table homeowner
    (homeowner_lname     varchar(15),
     homeowner_fname     varchar(15),
     customer_id         varchar(8) not null,
     street_address      varchar(40),
     primary key         (customer_id),
     foreign key         (street_address) references home(street_address)
                        on delete set null
    );