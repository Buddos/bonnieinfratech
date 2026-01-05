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
function checkLogin(event) {
  event.preventDefault();

  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  // Simple hardcoded login (for demo only!)
  if (username === "admin" && password === "1234") {
    window.location.href = "admin.html"; // redirect to admin page
  } else {
    document.getElementById("error").innerText = "Invalid login credentials!";
  }
}
