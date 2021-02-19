# __Vehicle API Docs__

### Create an order (POST request)

Request the API to create an order in the database and return the UUID order number.

URL: `<host site url>/api/create`  
Returns: `{ 'order_number': UUID order number }`  
On Fail Returns: `HttpResponse (status=500)`

### Update an order (POST request)

Request the API to update an order in the database with vehicle manufacturer, model and total price.

URL: `<host site url>/api/update/<order number>/?<parameters>`  
Parameters: All Optional, if none given no amendment will take place.
* `vehicle_manufacturer=<manufacturer value>`
* `model=<model value>`
* `total_price=<total price value>`
            
Returns: `HttpResonse (status=200)`  
On Fail Returns: `HttpResponse (status=500)`

### View an order (GET request)

Request the API to view a specific order in question.

URL: `<host site url>/api/view/<order number>`  
Returns: `{ 'order_number': UUID order number, 'vehicle_manufacturer': value,
 'model': value, 'total_price': value }`  
On Fail Returns: `HttpResponse (status=500)`

### View all orders (GET request)

Request the API to view all orders in the database.

URL: `<host site url>/api/view_all`  
Returns: `[{order 1}, {order 2}]`  
Each order will have the order number but not necessarily the other values.  
Format:`{ 'order_number': UUID order number, 'vehicle_manufacturer': value,
 'model': value, 'total_price': value }`   
On Fail Returns: `HttpResponse (status=500)`
