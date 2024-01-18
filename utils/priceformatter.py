def format_price(val):
    if val:
        return f'R$ {val:.2f}'.replace('.', ',')
    return None