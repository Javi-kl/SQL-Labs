#-- QUERIES (2025-12-27 / 2025-12-30)

#--1. Lista de todos los usuarios de 'Congo'
SELECT * FROM clientes WHERE pais='Congo';

#--2. ¿Cuántos usuarios tenemos exactamente en la DB?
SELECT COUNT(*) FROM clientes;

#--3. ¿Quién es el usuario con el id número 42?
SELECT nombre FROM clientes WHERE id=42;

#--4. ¿Qué usuarios se registraron después del 1 de Noviembre de 2024?
SELECT nombre,fecha_registro FROM clientes WHERE fecha_registro>'2024-01-11';

#--5. ¿Qué pedidos cuestan entre 50€ y 100€?
SELECT * FROM pedidos WHERE total BETWEEN 50 AND 100;

#--6. Busca usuarios cuyo nombre empiece por "M" o contenga "Garcia".
SELECT nombre FROM clientes WHERE nombre LIKE 'M%' OR nombre LIKE '%Garcia%'

#--7. ¿Cuál es la suma total (SUM) de dinero de todos los pedidos "Entregados"?
SELECT SUM(total) FROM pedidos WHERE estado='Entregado';

#--8. ¿Cuál es el precio promedio de venta en nuestra tienda?
SELECT AVG(total) FROM pedidos;

#--9.¿Cuántos usuarios hay por cada país? (De mayor a menor)
SELECT COUNT(*), pais FROM clientes GROUP BY pais ORDER BY COUNT(*) DESC; 

#--10. ¿Cuántos pedidos se hicieron por mes?
SELECT MONTH(fecha_pedido), COUNT(*) FROM pedidos GROUP BY MONTH(fecha_pedido) ORDER BY MONTH(fecha_pedido);

#--11. ¿Cuál es el pedido único más caro registrado?
SELECT MAX(total) FROM pedidos; 

#--12. Muestra una lista con: Nombre Usuario, Fecha Pedido, Total.
SELECT clientes.nombre, pedidos.fecha_pedido, pedidos.total
FROM clientes
INNER JOIN pedidos
ON clientes.id = pedidos.cliente_id;

#--13. ¿Qué usuarios existen pero NUNCA han comprado nada?
SELECT clientes.nombre
FROM clientes
LEFT JOIN pedidos ON clientes.id = pedidos.cliente_id
WHERE pedidos.cliente_id IS NULL;

#--14. ¿Quién es el cliente que más dinero ha gastado en total (suma de pedidos)?
SELECT clientes.nombre, SUM(pedidos.total) AS 'Total pedido'
FROM clientes
INNER JOIN pedidos ON clientes.id = pedidos.cliente_id
GROUP BY cliente_id 
ORDER BY SUM(pedidos.total) DESC 
LIMIT 1 ;

#--15. Muestra los 3 países que más dinero nos han generado.
SELECT clientes.pais,  SUM(pedidos.total) AS 'Total pais'
FROM clientes
INNER JOIN pedidos ON clientes.id = pedidos.cliente_id
GROUP BY clientes.pais
ORDER BY SUM(pedidos.total) DESC
LIMIT 3;








