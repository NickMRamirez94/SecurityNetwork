drop database if exists security;
create database security;
use security;

create table security_network
    (location       varchar(30),
     network_num    varchar(8),
     primary key    (network_num)
    );

create table employee
    (employee_id    varchar(8),
     lname          varchar(15),
     fname          varchar(15),
     primary key    (employee_id)
    );

create table home
    (name           varchar(15),
     contact        varchar(25),
     street_address varchar(40),
     primary key    (street_address)
    );

create table outdoor_camera
    (number         varchar(15),
     location       varchar(25),
     IP             varchar(10),
     name           varchar(15),
     primary key    (IP, name)
    );

create table camera_network
    (server_IP      varchar(10),
     network_id     varchar(8),
     primary key    (network_id)
    );

create table incident
    (instrusion_type    varchar(15),
     lost_equity        varchar(10),
     time               varchar(15),
     day                varchar(15),
     incident_id        varchar(8),
     primary key        (incident_id)
    ):

create table security_device
    (device_type        varchar(15),
     serial_no          varchar(15),
     device_IP          varchar(10),
     primary key        (serial_no, device_IP)
    );

create table homeowner
    (homeowner_lname     varchar(15),
     homeowner_fname     varchar(15),
     customer_id         varchar(8),
     primary key         (customer_id)
    );