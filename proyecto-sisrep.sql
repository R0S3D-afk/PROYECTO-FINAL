-- Crear base de datos
create database if not exists sistema_reparto;
use sistema_reparto;

-- Tabla de usuarios
create table usuarios (
    id int auto_increment primary key,
    nombre varchar(100) not null,
    email varchar(100) unique not null,
    contraseña varchar(255) not null,
    rol enum('administrador', 'cliente', 'repartidor') not null
);

-- Insertar datos de ejemplo en usuarios
insert into usuarios (nombre, email, contraseña, rol) values
('admin uno', 'admin1@example.com', 'adminpass1', 'administrador'),
('cliente uno', 'cliente1@example.com', 'clientepass1', 'cliente'),
('cliente dos', 'cliente2@example.com', 'clientepass2', 'cliente'),
('repartidor uno', 'repartidor1@example.com', 'repartidorpass1', 'repartidor'),
('repartidor dos', 'repartidor2@example.com', 'repartidorpass2', 'repartidor');

-- Tabla de pedidos
create table pedidos (
    id int auto_increment primary key,
    id_cliente int not null,
    direccion_entrega varchar(255) not null,
    contenido text,
    urgencia enum('alta', 'media', 'baja') not null,
    estado enum('pendiente', 'en_transito', 'entregado', 'cancelado') default 'pendiente',
    fecha_pedido timestamp default current_timestamp,
    foreign key (id_cliente) references usuarios(id)
);

-- Insertar datos de ejemplo en pedidos
insert into pedidos (id_cliente, direccion_entrega, contenido, urgencia) values
(2, '123 calle falsa, ciudad', 'documentos importantes', 'alta'),
(3, '456 avenida real, ciudad', 'paquete pequeño', 'media'),
(2, '789 pasaje libre, ciudad', 'medicamentos', 'alta'),
(3, '321 calle nueva, ciudad', 'juguetes', 'baja'),
(2, '654 plaza central, ciudad', 'libros', 'media');

-- Tabla de repartidores
create table repartidores (
    id int auto_increment primary key,
    id_usuario int not null,
    tipo_transporte enum('moto', 'bicicleta', 'a pie') not null,
    licencia varchar(50),
    foreign key (id_usuario) references usuarios(id)
);

-- Insertar datos de ejemplo en repartidores
-- Asegurarse de que los ids aquí coincidan con los ids utilizados en historialpedidos
insert into repartidores (id_usuario, tipo_transporte, licencia) values
(4, 'moto', 'lic12345'),
(5, 'bicicleta', null);

-- Tabla de historialpedidos
create table historialpedidos (
    id int auto_increment primary key,
    id_pedido int not null,
    id_repartidor int,
    fecha_entrega timestamp,
    estado enum('entregado', 'cancelado') not null,
    foreign key (id_pedido) references pedidos(id),
    foreign key (id_repartidor) references repartidores(id)
);

-- Insertar datos de ejemplo en historialpedidos
insert into historialpedidos (id_pedido, id_repartidor, fecha_entrega, estado) values
(1, 1, '2024-10-01 10:00:00', 'entregado'),
(2, 2, '2024-10-02 12:00:00', 'entregado'),
(3, 1, null, 'cancelado'),
(4, null, null, 'cancelado'),
(5, 2, '2024-10-03 09:30:00', 'entregado');

-- Tabla de calificaciones
create table calificaciones (
    id int auto_increment primary key,
    id_pedido int not null,
    id_cliente int not null,
    calificacion int check (calificacion between 1 and 5),
    comentario text,
    fecha timestamp default current_timestamp,
    foreign key (id_pedido) references pedidos(id),
    foreign key (id_cliente) references usuarios(id)
);

-- Insertar datos de ejemplo en calificaciones
insert into calificaciones (id_pedido, id_cliente, calificacion, comentario) values
(1, 2, 5, 'excelente servicio, muy rápido.'),
(2, 3, 4, 'buen servicio, aunque tardó un poco.'),
(5, 2, 3, 'servicio promedio, llegó en tiempo.'),
(1, 3, 4, 'buen servicio en general.'),
(2, 2, 5, 'muy rápido y amable el repartidor.');

select * from usuarios

