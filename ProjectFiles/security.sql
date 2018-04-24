drop database if exists security;
create database security;
use security;

create table security_network
    (loc            varchar(30),
     network_num    varchar(8) not null,
     primary key    (network_num)
    );

create table employee
    (employee_id    varchar(8) not null,
     lname          varchar(15),
     fname          varchar(15),
     username       varchar(45),
     pass           varchar(32),
     network_num    varchar(8),
     unique         (username),
     unique         (pass),
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
    (server_IP      varchar(13),
     network_id     varchar(8) not null,
     unique         (server_IP),
     primary key    (network_id)
    );

create table outdoor_camera
    (IP             varchar(10) not null,
     cam_name       varchar(40),
     street_address varchar(40),
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
     username            varchar(45),
     pass                varchar(32),
     unique              (username),
     unique              (pass),
     primary key         (customer_id),
     foreign key         (street_address) references home(street_address)
                        on delete set null
    );

INSERT security_network VALUES
('Kingsburg', '00987891'),
('San Francisco', '11435267');

INSERT employee VALUES
('74839654', 'Brassfield', 'David', 'dbfield12', 'David', '00987891'),
('35278908', 'Ramirez', 'Nicholas', 'nramirez', 'Nick', '11435267'),
('76454435', 'Curam', 'Ajay', 'acuram', 'Ajay', '11435267'),
('77789000', 'Jones', 'Julio' 'jjones', 'Julio', '00987891');

INSERT home VALUES
('Home 1', '(123) 123-4567', '255 Hayward Drive', '00987891'),
('Home 2', '(215) 777-8255', '8989 Dos Equis Lane', '00987891'),
('Home 3', '(510) 234-8989', '1212 Wayward Court', '11435267'),
('Home 4', '(925) 333-5645', '555 Greenville Drive', '11435267');

INSERT camera_network VALUES
('123.456.90.87', '87654564'),
('999.345.67.45', '99994453');

INSERT outdoor_camera VALUES
('546.888.34.54', '', '', ''),
('123.986.56.39', '', '', ''),
('165.990.89.01', '', '', ''),
('444.333.29.87', '', '', ''),
('324.091.90.89', '', '', ''),
('782.324.90.18', '', '', ''),
('098.178.89.22', '', '', ''),
('564.236.89.78', '', '', '');

INSERT incident VALUES
();

INSERT security_device VALUES
(),
(),
(),
();

INSERT homeowner VALUES
(),
(),
(),
();

