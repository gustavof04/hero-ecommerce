(function () {
    select_variation = document.getElementById('select-variation');
    variation_price = document.getElementById('variation-price');
    variation_promo_price = document.getElementById('variation-promo-price');

    if (!select_variation) {
        return;
    }

    if (!variation_price) {
        return;
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');
        promo_price = this.options[this.selectedIndex].getAttribute('data-promo-price');

        variation_price.innerHTML = price;

        if (variation_promo_price) {
            variation_promo_price.innerHTML = promo_price;
        }
    })
})();

