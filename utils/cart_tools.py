def cart_total_qnt(cart):
    return sum([item['quantity'] for item in cart.values()])


def cart_totals(cart):
    return sum(
        [
            item.get('quantitative_promo_price')
            if item.get('quantitative_promo_price')
            else item.get('quantitative_price')
            for item 
            in cart.values()
        ]
    )