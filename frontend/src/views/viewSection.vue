<template>
<div class="view-section-container">
        <h1>{{ section.name }}</h1>
        <p>{{ section.section_type }}</p>
  
        <h3>Products:</h3>
        <router-link :to="'/create_product?section_id=' + section.id" class="btn btn-primary">Create Product</router-link>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Manufacture Date</th>
              <th>Expiry Date</th>
              <th>Rate</th>
              <th>Unit</th>
              <th>Available Stock</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>{{ product.name }}</td>
              <td>{{ product.manufacture_date }}</td>
              <td>{{ product.expiry_date }}</td>
              <td>₹{{ product.rate }}/{{ product.unit }}</td>
              <td>{{ product.unit }}</td>
              <td>{{ product.available_stock }} {{ product.unit }}</td>
              <td>
                <router-link :to="'/edit_product' + product.id" class="btn btn-secondary">Edit</router-link>
                <router-link :to="'/delete_product' + product.id" class="btn btn-danger">Remove</router-link>
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
          name: '',
          section_type: '',
        },
        products: [],
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
}
</script>