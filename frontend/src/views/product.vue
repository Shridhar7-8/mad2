<template>
<div>
        <h1>{{ section.name }}</h1>
  
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Rate</th>
              <th>Available Stock</th>
              <th>Manufacture Date</th>
              <th>Expiry Date</th>
              <th>Quantity</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>{{ product.name }}</td>
              <td>₹{{ product.rate.toFixed(2) }}/{{ product.unit }}</td>
              <td>{{ product.available_stock }} {{ product.unit }}</td>
              <td>{{ formatDate(product.manufacture_date) }}</td>
              <td>{{ formatDate(product.expiry_date) }}</td>
              <td>
                <template v-if="product.available_stock > 0">
                  <form @submit.prevent="addToCart(product.id)">
                    <input type="number" v-model="quantity" min="1" :max="product.available_stock" value="1">
                    <button type="submit">Add to Cart</button>
                  </form>
                </template>
                <span v-else>Out of Stock</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
</template>
<script>
export default{
    data() {
      return {
        section: {
          name: "",
        },
        products: [],
        quantity: 1,
      };
    },
    created() {
        const sectionId = parseInt(this.$route.params.sectionId);

        fetch(`/api/sections/${sectionId}`)
            .then((response) => response.json())
            .then((data) => {
                this.section = data;
            })
            .catch((error) => {
                console.error(error);
            });

        fetch(`/api/products?section_id=${sectionId}`)
            .then((response) => response.json())
            .then((data) => {
              this.products = data;
            })
            .catch((error) => {
              console.error(error);
            });
    },
    methods: {
      addToCart(productId) {
        fetch(`/api/add_to_cart/${productId}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ quantity }),
            })
            .then((response) => {
              if (!response.ok) {
                throw new Error("Failed to add the product to the cart");
              }
              return response.json();
            })
            .then((data) => {
                console.log(data);
                alert("Product added to the cart successfully");
            })
            .catch((error) => {
                console.error(error);
                alert("Failed to add the product to the cart");
            });
        },
        formatDate(dateString) {
        const date = new Date(dateString);
        return date.toISOString().split("T")[0];
        },
    },
}
</script>