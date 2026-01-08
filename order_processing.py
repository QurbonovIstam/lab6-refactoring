# order_processing.py

DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21


def parse_request(request: dict):
    return (
        request.get("user_id"),
        request.get("items"),
        request.get("coupon"),
        request.get("currency") or DEFAULT_CURRENCY
    )


def validate_request(user_id, items):
    if user_id is None:
        raise ValueError("user_id is required")

    if not isinstance(items, list):
        raise ValueError("items must be a list")

    if len(items) == 0:
        raise ValueError("items must not be empty")

    for item in items:
        if "price" not in item or "qty" not in item:
            raise ValueError("item must have price and qty")
        if item["price"] <= 0:
            raise ValueError("price must be positive")
        if item["qty"] <= 0:
            raise ValueError("qty must be positive")


def calculate_subtotal(items):
    return sum(item["price"] * item["qty"] for item in items)


def calculate_discount(subtotal, coupon):
    if not coupon:
        return 0

    if coupon == "SAVE10":
        return int(subtotal * 0.10)

    if coupon == "SAVE20":
        if subtotal >= 200:
            return int(subtotal * 0.20)
        return int(subtotal * 0.05)

    if coupon == "VIP":
        return 50 if subtotal >= 100 else 10

    raise ValueError("unknown coupon")


def calculate_tax(amount):
    return int(amount * TAX_RATE)


def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = parse_request(request)
    validate_request(user_id, items)

    subtotal = calculate_subtotal(items)
    discount = calculate_discount(subtotal, coupon)

    total_after_discount = max(subtotal - discount, 0)
    tax = calculate_tax(total_after_discount)
    total = total_after_discount + tax

    order_id = f"{user_id}-{len(items)}-X"

    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }
