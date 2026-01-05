// ===== main.js =====
// BonnieInfratech Solutions
// Handles dynamic product loading, admin uploads, and basic UI interactions

document.addEventListener("DOMContentLoaded", () => {
  const productList = document.getElementById("product-list") || document.querySelector(".products");

  // Load products dynamically from JSON file
  fetch("assets/products.json")
    .then(response => {
      if (!response.ok) throw new Error("Failed to fetch product data");
      return response.json();
    })
    .then(products => {
      if (!Array.isArray(products) || products.length === 0) {
        if (productList) productList.innerHTML = "<p>No products available at the moment.</p>";
        return;
      }

      if (productList) productList.innerHTML = ""; // Clear old content

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
      if (productList)
        productList.innerHTML = "<p style='color:red;'>Unable to load products. Please try again later.</p>";
    });

  // ===== Admin Upload Section (Optional) =====
  const uploadForm = document.getElementById("uploadForm");
  if (uploadForm) {
    uploadForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const fileInput = document.getElementById("machineryImage");
      const nameInput = document.getElementById("machineryName");

      if (!fileInput.files.length || !nameInput.value.trim()) {
        alert("Please select an image and enter a name.");
        return;
      }

      const file = fileInput.files[0];
      const reader = new FileReader();

      reader.onload = () => {
        const newProduct = {
          name: nameInput.value,
          description: "New product uploaded by admin",
          image: reader.result
        };

        // Display it instantly in admin preview (optional)
        const gallery = document.getElementById("machineryGallery");
        if (gallery) {
          const img = document.createElement("img");
          img.src = reader.result;
          img.alt = nameInput.value;
          img.style.width = "150px";
          img.style.margin = "10px";
          gallery.appendChild(img);
        }

        // Save product to local storage (client-side)
        const storedProducts = JSON.parse(localStorage.getItem("products")) || [];
        storedProducts.push(newProduct);
        localStorage.setItem("products", JSON.stringify(storedProducts));

        alert("Product added successfully!");
        fileInput.value = "";
        nameInput.value = "";
      };

      reader.readAsDataURL(file);
    });
  }

  // ===== Load Products from Local Storage (for admin preview / testing) =====
  const storedProducts = JSON.parse(localStorage.getItem("products")) || [];
  if (storedProducts.length && productList) {
    storedProducts.forEach(product => {
      const card = document.createElement("div");
      card.className = "product";
      card.innerHTML = `
        <img src="${product.image}" alt="${product.name}">
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <button class="buy-btn">Buy Now</button>
      `;
      productList.appendChild(card);
    });
  }
});
document.addEventListener("DOMContentLoaded", () => {
  const userRole = localStorage.getItem("userRole"); // e.g., "admin" or "customer"
  const adminLink = document.querySelector(".admin-link");

  if (userRole !== "admin" && adminLink) {
    adminLink.style.display = "none";
  }
});
