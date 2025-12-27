### SINTAXIS BASICA

1. Lista de todos los usuarios de 'Congo'
``
SELECT * FROM usuarios WHERE pais='Congo';
``

2. ¿Cuántos usuarios tenemos exactamente en la DB?
``
SELECT COUNT(*) FROM usuarios;
``

3. ¿Quién es el usuario con el id número 42?
``
SELECT nombre FROM usuarios WHERE id=42;
``

4. ¿Qué usuarios se registraron después del 1 de Noviembre de 2024?
``
SELECT nombre,fecha_registro FROM usuarios WHERE fecha_registro>'2024-01-11';
``

5. ¿Qué pedidos cuestan entre 50€ y 100€?
``
SELECT * FROM pedidos WHERE total BETWEEN 50 AND 100;
``

6. Busca usuarios cuyo nombre empiece por "M" o contenga "Garcia".
``
SELECT nombre FROM usuarios WHERE nombre LIKE 'M%' OR nombre LIKE '%Garcia%'