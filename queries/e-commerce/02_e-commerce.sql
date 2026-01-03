#-- QUERIES (2026-01-03 /  ....)

#--16. ¿Cuál es el ticket medio (promedio de gasto) por usuario?
#--(Queremos saber cuánto gasta de media cada cliente real,
#-- no el promedio de todos los pedidos sueltos).
SELECT clientes.nombre, clientes.id, AVG(pedidos.total) AS 'Ticket medio de gasto'
FROM clientes
INNER JOIN pedidos
ON clientes.id = pedidos.usuario_id
GROUP BY clientes.id, clientes.nombre
ORDER BY AVG(pedidos.total) DESC;

#--17. Informe de inventario: ¿Qué productos tienen menos de 5 unidades en stock?
#--(Esencial para saber qué reponer urgentemente).
SELECT productos.nombre AS producto, productos.stock
FROM productos
WHERE stock < 10
ORDER BY stock;

#--18. Ventas del "Q4" (Cuarto Trimestre): ¿Cuánto vendimos en total en Octubre, Noviembre y Diciembre?
#--(Seleccionar todos los pedidos del Q4, (CORREGIR al actualizar el total)) !AÑADE COLUMNA SUM(total).
SELECT pedidos.usuario_id, pedidos.fecha_pedido
FROM pedidos 
WHERE fecha_pedido BETWEEN '2025-09-30' AND '2025-12-30';

#--19. ¿Qué porcentaje de nuestros pedidos han sido cancelados?
#--(Esta es difícil: requiere contar los cancelados y dividir por el total de pedidos).
SELECT (AVG(estado = 'cancelado') * 100) AS 'porcentaje cancelación'
FROM pedidos;


#--20. Clasificación de clientes: Muestra el nombre y una etiqueta 'VIP' si han gastado más de 200€, o 'Regular' si no.
#--(Pista: Investiga la función CASE WHEN o IF dentro del SELECT).
SELECT clientes.nombre, SUM(pedidos.total) AS 'Gasto total',
CASE
	WHEN SUM(pedidos.total) > 100 THEN 'VIP'
	ELSE 'REGULAR'
END AS 'Clasificación de clientes'
FROM clientes
INNER JOIN pedidos
ON clientes.id = pedidos.usuario_id
GROUP BY clientes.id, clientes.nombre;






