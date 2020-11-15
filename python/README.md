# Backend challenge VLC

### General

* Stub classes has been coded in order to test E-Mails, printing labels, subscriptions... 
They can be easily replaced by implemented classes using the same interface.
* Use of pytest syntax for assertions. It's really simple to read what do you expect from a test.
* The main script can be interpreted as an acceptance test, I followed the same way to define the rest of use cases.
* Most of the data holder classes could be coded as `namedTuple` or `dataclass`(python3.8), this could
avoid the boilerplate of `__eq__`, `__repr__`, `__hash__`... etc.
* Acceptance test preparation are not readable and they are quite the same as order tests.

### bootstrap.py

* All static attributes has been deleted because they were being used as instance attributes.
Missing attributes has been added in constructors.
* The use of mutable instances as part of a default argument are discouraged because every instance 
that uses the default value will use the same mutable instance.
```python
def f(attributes={}):
    if 'key' in attributes:
        raise(RuntimeError)
    attributes['key'] = 'value'

f()
f() # Raises RuntimeError
```
* For the "same" reason `time.time()` has been deleted from default arguments:
```python
import time

def print_time(t=time.time()):
    print(f'{t}')

print_time() # prints 1605497193.5833664
time.sleep(1)
print_time() # prints 1605497193.5833664
```
* Methods like `order.total_amount()` has been replaced to properties (`order.total_amount`), 
it increases code readability.
* `Order.add_product` has been changed to add an `OrderItem` for a given `Product` and `quantity`.
* `Order.total_amount` function has been refactored in a pythonic way, it's more readable and simple.
* Instead of searching the items doing a for loop every time, items by type has been exposed in `Order`.
* In my honest opinion, I think it's better to extract the logical busyness from data holder classes like`Payment`
and keep them simple. That's why I created `order_service.pay(...)`.
* `Payment.is_paid` has been removed. Now `Order` exposes `is_paid` attribute.
* `OrderItem.total` now returns the product price * quantity.
* The evaluation of`.is_paid` has been changed according to [PEP8](https://www.python.org/dev/peps/pep-0008/#programming-recommendations).

## Usage
```shell script
## Requires pytest. (pip install pytest)
cd python
pytest . -v
```
