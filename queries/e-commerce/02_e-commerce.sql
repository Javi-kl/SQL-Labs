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


#--21. "Calcula cuánto costaba cada unidad del producto en el momento de la venta 
#--basándote en el subtotal pagado, y compáralo con el precio actual del catálogo."

SELECT 



#--22. La Cesta de la Compra Más Grande
#--"¿Cuál es el pedido que ha tenido más artículos distintos dentro?"

SELECT COUNT(DISTINCT dp.producto_id) AS 'Productos_distintos'
FROM detalles_pedidos dp
GROUP BY pedido_id
ORDER BY Productos_distintos DESC
LIMIT 1;

#--23. "¿Qué producto se compra más veces, pero en cantidad de 1 sola unidad?"

SELECT  p.nombre AS 'Producto', COUNT(dp.id) AS 'Veces_comprado_suelto'
FROM detalles_pedidos dp 
INNER JOIN productos p ON dp.producto_id = p.id 
WHERE dp.cantidad = 1
GROUP BY p.nombre
ORDER BY Veces_comprado_suelto DESC
LIMIT 1;




