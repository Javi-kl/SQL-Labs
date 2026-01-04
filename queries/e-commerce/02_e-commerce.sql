#-- QUERIES (2026-01-03 /  ....)

#--16. ¿Cuál es el ticket medio (promedio de gasto) por usuario?
#--(Queremos saber cuánto gasta de media cada cliente real,
SELECT clientes.nombre, clientes.id, AVG(pedidos.total) AS 'Ticket medio de gasto'
FROM clientes
INNER JOIN pedidos
ON clientes.id = pedidos.cliente_id
GROUP BY clientes.id, clientes.nombre
ORDER BY AVG(pedidos.total) DESC;

#--17. Informe de inventario: ¿Qué productos tienen menos de 5 unidades en stock?
SELECT productos.nombre AS producto, productos.stock
FROM productos
WHERE stock < 10
ORDER BY stock;

#--18. Ventas del "Q4" (Cuarto Trimestre): ¿Cuánto vendimos en total en Octubre, Noviembre y Diciembre?
#--(Seleccionar todos los pedidos del Q4, (CORREGIR al actualizar el total)) !AÑADE COLUMNA SUM(total).
SELECT pedidos.cliente_id, pedidos.fecha_pedido, SUM(pedidos.total)
FROM pedidos 
WHERE fecha_pedido BETWEEN '2025-09-30' AND '2025-12-30'
GROUP BY pedidos.cliente_id;

#--19. ¿Qué porcentaje de nuestros pedidos han sido cancelados?
SELECT (AVG(estado = 'cancelado') * 100) AS 'porcentaje cancelación'
FROM pedidos;


#--20. Clasificación de clientes: Muestra el nombre y una etiqueta 'VIP' si han gastado más de 200€, o 'Regular' si no.
SELECT clientes.nombre, SUM(pedidos.total) AS 'Gasto total',
CASE
	WHEN SUM(pedidos.total) > 100 THEN 'VIP'
	ELSE 'REGULAR'
END AS 'Clasificación de clientes'
FROM clientes
INNER JOIN pedidos
ON clientes.id = pedidos.cliente_id
GROUP BY clientes.id, clientes.nombre;








