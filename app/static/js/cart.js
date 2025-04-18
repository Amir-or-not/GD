// окно для корзины
document.addEventListener('DOMContentLoaded', function () {
  const cartIcon = document.querySelector('.cart-icon');
  const dropdown = cartIcon.querySelector('.cart-dropdown');

  cartIcon.addEventListener('click', function (e) {
    e.stopPropagation();
    dropdown.style.display = dropdown.style.display === 'flex' ? 'none' : 'flex';
  });

  cartIcon.addEventListener('dblclick', function () {
    window.location.href = '/cart/';
  });

  document.addEventListener('click', function (e) {
    if (!cartIcon.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });
});
