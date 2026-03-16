const categoryLinks = document.querySelectorAll(".category-link");
const products = document.querySelectorAll(".product-card");

categoryLinks.forEach(link => {
  link.addEventListener("click", function(e) {
    e.preventDefault();

    const categoryId = this.dataset.category;

    categoryLinks.forEach(l => l.classList.remove("active"));
    this.classList.add("active");

    products.forEach(product => {

      if (categoryId === "all") {
        product.style.display = "block";
        return;
      }

      if (product.dataset.category === categoryId) {
        product.style.display = "block";
      } else {
        product.style.display = "none";
      }
    });
  });
});


function addToCart(productId) {
  fetch("/add_to_cart", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ product_id: productId })
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.message);
  });
}