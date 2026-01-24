#-- QUERIES (2026-1-17 / )

#-- 1. ¿Cuántos productos tenemos con stock = 0?
SELECT p.nombre, p.stock 
FROM productos p
WHERE stock = 0;

#-- 2. Muestra los pedidos realizados en el año 2025
SELECT pe.id, pe.fecha_pedido 
FROM pedidos pe
WHERE YEAR(fecha_pedido) = '2025';


#-- 3. Lista los productos cuyo precio sea mayor a 50€ Y menor a 100€
SELECT p.nombre, p.precio
FROM productos p
WHERE precio > 50 
AND precio < 100;

#-- 4. ¿Cuántos pedidos hay por cada estado? (Muestra también los que tienen 0)
SELECT p.estado, COUNT(*)
FROM pedidos p
GROUP BY estado;

#-- 5. Lista los nombres de clientes en MAYÚSCULAS
SELECT UPPER(c.nombre)
FROM clientes c;

#-- 6. Muestra el día de la semana (nombre) en que se registró cada cliente
SELECT DAYNAME(c.fecha_registro) AS 'Dia de la semana',c.id
FROM clientes c; 

#-- 7. ¿Qué productos tienen un precio de 19.99, 29.99 o 39.99?
SELECT p.nombre, p.precio
FROM productos p
WHERE p.precio IN(19.99,29.99,39.99,79.92);

#-- 8. Muestra los primeros 5 caracteres del email de cada cliente
SELECT c.nombre, LEFT(email,5)
FROM clientes c;

#-- 9. ¿Cuántos pedidos hay por cada año?
SELECT COUNT(*)AS 'Cantidad', YEAR(p.fecha_pedido) AS 'Año'
FROM pedidos p 
GROUP BY YEAR(p.fecha_pedido);


#-- 10. Lista los clientes cuyo país NO sea 'España' ni 'Francia'
SELECT c.nombre
FROM clientes c
WHERE c.pais NOT IN('España','Francia','Suiza');









