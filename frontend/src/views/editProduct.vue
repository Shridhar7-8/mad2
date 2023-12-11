<template>
<div class="edit-product-container">
        <h1>Edit Product</h1>
        <form @submit.prevent="updateProduct">
          <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" v-model="product.name" required>
          </div>
          <div class="form-group">
            <label for="manufacture_date">Manufacture Date:</label>
            <input type="date" id="manufacture_date" v-model="product.manufacture_date" required>
          </div>
          <div class="form-group">
            <label for="expiry_date">Expiry Date:</label>
            <input type="date" id="expiry_date" v-model="product.expiry_date" required>
          </div>
          <div class="form-group">
            <label for="rate">Rate:</label>
            <input type="number" id="rate" v-model="product.rate" step="0.01" required>
          </div>
          <div class="form-group">
            <label for="unit">Unit:</label>
            <select id="unit" v-model="product.unit" required>
              <option value="kg">/kg</option>
              <option value="g">/g</option>
              <option value="litre">/litre</option>
              <option value="ml">/ml</option>
              <option value="piece">/piece</option>
            </select>
          </div>
          <div class="form-group">
            <label for="available_stock">Available Stock:</label>
            <input type="number" id="available_stock" v-model="product.available_stock" required>
          </div>
          <div class="form-group">
            <label for="section">Section:</label>
            <select id="section" v-model="product.section_id" required>
              <option v-for="section in sections" :value="section.id">{{ section.name }}</option>
            </select>
          </div>
          <button type="submit">Update</button>
        </form>
      </div>
</template>
<script>
export default{
    data() {
      return {
        product: {
          name: '',
          manufacture_date: '',
          expiry_date: '',
          rate: 0,
          unit: 'kg',
          available_stock: 0,
          section_id: null,
        },
        sections: [], 
      };
    },
    created() {
      
      fetch('http://127.0.0.1:5000/api/sections')
        .then((response) => response.json())
        .then((data) => {
          this.sections = data;
        })
        .catch((error) => {
          console.error(error);
        });
  
      
      const productId = parseInt(this.$route.params.productId);
      fetch(`http://127.0.0.1:5000/api/products/${productId}`)
        .then((response) => response.json())
        .then((data) => {
          this.product = data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    methods: {
      updateProduct() {
        
        fetch(`http://127.0.0.1:5000/api/products/${this.product.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.product),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error('Failed to update product');
            }
            return response.json();
          })
          .then((data) => {
            
            console.log(data);
            alert('Product updated successfully');
          })
          .catch((error) => {
            
            console.error(error);
          });
      },
    },
}
</script>