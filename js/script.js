// Handle product order
function orderProduct(productName) {
  alert(`You have ordered: ${productName}. Our team will contact you.`);
}

// Handle admin adding product (localStorage)
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("addProductForm");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = document.getElementById("productName").value;
      const price = document.getElementById("productPrice").value;
      alert(`New product added: ${name} - ${price}`);
      form.reset();
    });
  }
});
