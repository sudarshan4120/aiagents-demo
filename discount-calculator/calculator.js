function calculateDiscount(price, customerType, on_clearance) {
  if (price < 0) {
    throw new Error('Price cannot be negative');
  }

  let discountedPrice;

  if (on_clearance) {
    discountedPrice = price * (1 - 0.30);
  } else {
    const discountRates = {
      regular: 0,
      member: 0.10,
      vip: 0.20
    };

    const discount = discountRates[customerType] || 0;
    discountedPrice = price * (1 - discount);
  }

  return Math.round(discountedPrice * 100) / 100;
}

module.exports = calculateDiscount;