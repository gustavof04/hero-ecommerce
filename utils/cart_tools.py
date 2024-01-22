def cart_total_qnt(cart):
    return sum([item['quantity'] for item in cart.values()])