// ===== main.js =====
// BonnieInfratech Solutions
// Handles dynamic product loading and basic UI interactions

document.addEventListener("DOMContentLoaded", () => {
  const productList = document.getElementById("product-list");

  // Load products from JSON
  fetch("assets/products.json")
    .then(response => {
      if (!response.ok) throw new Error("Failed to fetch product data");
      return response.json();
    })
    .then(products => {
      if (!Array.isArray(products) || products.length === 0) {
        productList.innerHTML = "<p>No products available at the moment.</p>";
        return;
      }

      products.forEach(product => {
        const productCard = document.createElement("div");
        productCard.className = "product";

        productCard.innerHTML = `
          <img src="${product.image}" alt="${product.name}">
          <h3>${product.name}</h3>
          <p>${product.description}</p>
          <button class="buy-btn">Buy Now</button>
        `;

        productList.appendChild(productCard);
      });
    })
    .catch(err => {
      console.error("Error loading products:", err);
      productList.innerHTML = "<p style='color:red;'>Unable to load products. Please try again later.</p>";
    });
});
