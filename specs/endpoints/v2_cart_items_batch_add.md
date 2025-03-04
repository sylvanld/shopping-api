## Add a batch of items to a shopping cart

This endpoint allowing marking multiple items as picked.

## Specification
**Endpoint**

```
PUT /v2/carts/{cartID}/items/batch
```

**Payload**
```json
{
    "items": [
        {
            "itemID": "1234",
            "itemUnit": "g",
            "itemQuantity": 3,
            "operationID": "XYZ"
        }
    ]
}
```

**Response Codes**

| HTTP Status Code | Meaning                                                                  |
| ---------------- | ------------------------------------------------------------------------ |
| 202              | If submitted operations were accepted                                    |
| 409              | If lock acquisition failed, meaning API is processing another operation. |

## Implementation

### Prevent duplicates between users

We want to avoid 2 users picking the same items without them to be aware. So the endpoint should answer negatively if the quantity of an item in the cart after accepting an operation becomes negative (or creates a duplicate for items without quantity).

In order to avoid race conditions, the endpoint `PUT /v2/carts/{cartID}/items/batch` should include a distributed locking mechanism that prevent multiple users from editing the same shopping cart items simultaneously.

### Mitigating poor connectivity issues

Instead of directly calling the `PUT /v2/carts/{cartID}/items/batch` endpoint, the frontend will store items operations in a queue. Then while the queue is not empty, a background process is responsible to forward this queue (by batch) to the shopping API.

This process ensures operations are replayed if connectivity is lost.

It may happens that backend lose connection after storing operations on items. So backend should store an `operationID` and still answer positively if operation is already registered.

### Store operations along with cart items

Previously, when trying to update an item, we directly updated given item's quantity field. This would lead to duplication in case of a connectivity issue were request is replayed. In order to be able to detect it, we need to store operations in database.

## Client-Side usage

Clients should implement an exponential backoff strategy with jitter when receiving a locked response:

1. Start with a base wait time (e.g., 100ms).
2. For each retry:
   - Multiply wait time by a factor (e.g., 2).
   - Add random jitter (e.g., 0-100ms).
   - Cap wait time at a maximum value (e.g., 5 seconds).
3. Retry the request after waiting.
4. Set a maximum number of retries.
