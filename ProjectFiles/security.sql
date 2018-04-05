drop database if exists security;
create database security;
use security;

create table security_network
    (loc            varchar(30),
     network_num    varchar(8),
     primary key    (network_num)
    );

create table employee
    (employee_id    varchar(8),
     lname          varchar(15),
     fname          varchar(15),
     network_num    varchar(8),
     primary key    (employee_id),
     foreign key    (network_num) references security_network(network_num)
    );

create table home
    (home_name      varchar(15),
     contact        varchar(15),
     street_address varchar(40),
     network_num    varchar(8),
     primary key    (street_address),
     foreign key    (network_num) references security_network(network_num)
    );

create table camera_network
    (server_IP      varchar(10),
     network_id     varchar(8),
     primary key    (network_id)
    );

create table outdoor_camera
    (num            int,
     loc            varchar(25),
     IP             varchar(10),
     cam_name       varchar(15),
     street_address varchar(40),
     unique         (number),
     network_id     varchar(8),
     primary key    (IP),
     foreign key    (street_address) references home(street_address),
     foreign key    (network_id) references camera_network(network_id)
    );

create table incident
    (instrusion_type    varchar(15),
     lost_equity        varchar(10),
     occured_time       time,
     day                date,
     incident_id        varchar(8),
     street_address     varchar(40),
     network_id         varchar(8),
     primary key        (incident_id),
     foreign key        (street_address) references home(street_address),
     foreign key        (network_id) references camera_network(network_id)
    ):

create table security_device
    (device_type        varchar(15),
     serial_no          varchar(15),
     device_IP          varchar(10),
     street_address     varchar(40),
     primary key        (serial_no, device_IP),
     foreign key        (street_address) references home(street_address)
    );

create table homeowner
    (homeowner_lname     varchar(15),
     homeowner_fname     varchar(15),
     customer_id         varchar(8),
     street_address      varchar(40),
     primary key         (customer_id),
     foreign key         (street_address) references home(street_address)
    );