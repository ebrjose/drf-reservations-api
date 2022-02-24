# Api de reservas con DRF

Utilizando Django REST Framework, desarrollá los endpoints para el sistema de reservas de habitación de un hotel.
CONDICIONES:
- Las reservas pueden tener 3 estados: Pendiente, Pagado y Eliminado.
- Los datos a almacenar para la reserva son: los detalles del cuarto reservado, los días de estadía, los datos de facturación e identificación del cliente, el monto pagado y el método de pago.
- Proponé los endpoints a crearse para tratar de cubrir el flujo normal de operación de reserva y explicar por qué.

# Contenido
1. [Instalación](#Instalación)
2. [Procedimiento](#Procedimiento)
3. [Testing](#Testing)
4. [Documentación](#Documentación)


# Instalación
```bash
# Instalamos dependencias
$ python -m venv <env path>
$ source <virtual env path>/bin/activate
$ pip install -r requirements.txt

# Ejecutamos las migraciones
$ python manage.py migrate

# Ejecutamos el servidor
$ python manage.py runserver

```


# Procedimiento

## Paso 1 : Registrar habitaciones
> Las habitaciones se pueden registrar en el **endpoint**.
>
> **POST** | http://127.0.0.1:8000/api/rooms/
> 
>  El tipo de habitación puede tener los siguientes valores: type = SIMPLE | DOUBLE | SUITE


**Request:**

``` bash
curl --location --request POST 'http://127.0.0.1:8000/api/rooms/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "SIMPLE",
    "description": "Room with SIMPLE bed",
    "price": "10"
}'
```

**Response:**
```json
{
    "id": 2,
    "type": "SIMPLE",
    "description": "Room with SIMPLE bed",
    "price": 10,
    "available": true
}
```

## Paso 2 : Registrar un huesped

> Los Huéspedes se registran en el **endpoint**.
>
> **POST** |   http://127.0.0.1:8000/api/users/register/

**Request:**
``` bash
curl --location --request POST 'http://127.0.0.1:8000/api/users/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "ebrjose",
    "email": "ebrjose@gmail.com",
    "name": "Eber",
    "last_name": "Coaquira"
}'
```

**Response:**
```json
{
    "id": 2,
    "username": "ebrjose",
    "email": "ebrjose@gmail.com",
    "name": "Eber",
    "last_name": "Coaquira"
}
```

## Paso 3 : Realizar una reservación

> Las reservaciones se realizan en el **endpoint**.
>
> **POST** |   http://127.0.0.1:8000/api/reservations/make/

**Validaciones:**
* No se pueden reservar fechas anteriores a la de hoy.
* La fecha de salida no puede ser menor a la fecha de entrada.
* No se puede reservar una habitacion ocupada. 

**Request:**
``` bash
curl --location --request POST 'http://127.0.0.1:8000/api/reservations/make/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "guest": "1",
    "room": "1",
    "checkin_date": "2022-05-23",
    "checkout_date": "2021-05-30"
}'
```

**Response:**
```json
{
    "id": 6,
    "uuid": "gpHE2i7Dv2rpBEqmvZJeCf",
    "reservation_date": "2022-02-24T06:03:23.597316Z",
    "checkin_date": "2022-05-25",
    "checkout_date": "2022-05-30",
    "guest": "Eber Coaquira",
    "room": "2 | SIMPLE |  Habitación simple",
    "price_per_night": 50,
    "total_nights": 5,
    "room_charge": 250,
    "taxes": 32.5,
    "total": 282.5,
    "status": "PENDING"
}
```

## Paso 4 : Procesar el pago de una reserva

> Los pagos se procesan en el **endpoint**.
>
> **POST** |  http://127.0.0.1:8000/api/payments/process/
>
**Validaciones:**
* Cuando el pago es procesado el estado de la reservacion cambia a **PAID**
* Solo se pueden pagar las reservas con estado PENDING
* El estado de la habitación cambia a disponible

**Request:**
``` bash

# El metodo de pago puede ser
# payment_method = CREDIT_CARD | CASH | PAYPAL

curl --location --request POST 'http://127.0.0.1:8000/api/payments/proccess/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "reservation": "1",
    "payment_method": "CREDIT_CARD",
    "total": 113.0
}'
```

**Response:**
```json
{
    "id": 2,
    "guest": {
        "id": 1,
        "username": "ebrjose",
        "email": "ebrjose@gmail.com",
        "name": "Eber",
        "last_name": "Coaquira"
    },
    "reservation": {
        "id": 1,
        "uuid": "j2D7jheYvwioksJRGTFrmu",
        "reservation_date": "2022-02-24T04:39:18.042003Z",
        "checkin_date": "2022-04-23",
        "checkout_date": "2022-04-25",
        "total_nights": 2,
        "guest": "Eber Coaquira",
        "room": "1 | SIMPLE | Available | Habitación simple"
    },
    "uuid": "iHfhFdA6JV5F4Qhn9nFheH",
    "payment_method": "CREDIT_CARD",
    "taxes": "13.00",
    "room_charge": "100.00",
    "total": "113.00",
    "payment_date": "2022-02-24"
}
```


## Opcional : Cancelar una reservación

> Las reservaciones se cancelan en el **endpoint**.
>
> **PATCH** |  http://127.0.0.1:8000/api/reservations/:id/cancel/
>
> Cuando se Cancela una reserva el estado de la reserva cambia a **CANCELLED**

**Request:**
``` bash
curl --location --request PATCH 'http://127.0.0.1:8000/api/reservations/1/cancel/'
```


**Response:**
```json
{
    "id": 1,
    "status": "CANCELLED",
    "guest": {
        "id": 1,
        "username": "ebrjose",
        "email": "ebrjose@gmail.com",
        "name": "Eber",
        "last_name": "Coaquira"
    }
}
```

# Testing
> Para ejecutar las pruebas

``` bash
$ python manage.py test -v 2
```

**Resultado:**

``` bash
$ python manage.py test -v 2
...
...
System check identified no issues (0 silenced).
test_paid_reservations_cannot_be_processed_again (tests.integration.payments.test_process_payments.TestsProcessPayments) ... ok
test_process_payment (tests.integration.payments.test_process_payments.TestsProcessPayments) ... ok
test_wrong_amount_should_not_process_the_payment (tests.integration.payments.test_process_payments.TestsProcessPayments) ... ok
test_cannot_make_a_reservation_without_data (tests.integration.reservations.test_create_reservation.CreateReservationsTest) ... ok
test_checkin_date_must_be_greater_than_or_equal_to_today (tests.integration.reservations.test_create_reservation.CreateReservationsTest) ... ok
test_checkout_date_must_be_greater_than_or_equal_to_checkin_date (tests.integration.reservations.test_create_reservation.CreateReservationsTest) ... ok
test_only_available_rooms_can_be_reserved (tests.integration.reservations.test_create_reservation.CreateReservationsTest) ... ok
test_room_can_be_unavailable_after_reservation (tests.integration.reservations.test_create_reservation.CreateReservationsTest) ... ok
test_room_can_be_registered_with_data (tests.integration.rooms.test_create_rooms.CreateRoomsTest) ... ok
test_room_can_be_registered_without_field_type (tests.integration.rooms.test_create_rooms.CreateRoomsTest) ... ok
test_room_cannot_be_registered_without_data (tests.integration.rooms.test_create_rooms.CreateRoomsTest) ... ok
test_can_fetch_a_single_room (tests.integration.rooms.test_list_rooms.ListRoomsTest) ... ok
test_can_fetch_all_rooms (tests.integration.rooms.test_list_rooms.ListRoomsTest) ... ok
test_user_can_be_registered (tests.integration.users.test_create_users.CreateUsersTestUsers) ... ok
test_user_cannot_be_registered_with_existent_email (tests.integration.users.test_create_users.CreateUsersTestUsers) ... ok
test_user_cannot_be_registered_without_data (tests.integration.users.test_create_users.CreateUsersTestUsers) ... ok
test_can_fetch_a_single_user (tests.integration.users.test_list_users.ListUsersTest) ... ok
test_can_fetch_all_rooms (tests.integration.users.test_list_users.ListUsersTest) ... ok

----------------------------------------------------------------------
Ran 18 tests in 0.086s

OK


```

# Documentación
- **POSTMAN**

    [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/1075652-81d85f3e-5fe4-4162-a89a-d72fe8ba0307?action=collection%2Ffork&collection-url=entityId%3D1075652-81d85f3e-5fe4-4162-a89a-d72fe8ba0307%26entityType%3Dcollection%26workspaceId%3D18b7d875-c0ac-4941-823a-740a329b7f3c)

 **WorkSpace:**
    https://www.postman.com/crimson-space-47296/workspace/tu-gerente/request/1075652-cad34cd7-e7d0-41bd-86b1-932d8288b38c



[comment]: <> (- **SWAGER**)

[comment]: <> (    http://127.0.0.1:8000/swagger/)
