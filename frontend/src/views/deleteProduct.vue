<template>
<div class="delete-product-container">
        <h2>Delete Product</h2>
        <p>Are you sure you want to delete the following product?</p>
        <h4>{{ product.name }}</h4>
        <p><strong>Manufacture Date:</strong> {{ product.manufacture_date }}</p>
        <p><strong>Expiry Date:</strong> {{ product.expiry_date }}</p>
        <p><strong>Rate:</strong> {{ product.rate }}/{{ product.unit }}</p>
        <p><strong>Unit:</strong> {{ product.unit }}</p>
        <form @submit.prevent="confirmDelete">
          <input type="hidden" name="confirm_delete" value="true">
          <button type="submit" class="btn btn-danger">Confirm Deletion</button>
          <router-link to="/admindashboard" class="btn btn-secondary">Cancel</router-link>
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
          unit: '',
        },
      };
    },
    created() {
      
      const productId = parseInt(this.$route.params.productId);
      fetch(`/api/products/${productId}`)
        .then((response) => response.json())
        .then((data) => {
          this.product = data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    methods: {
      confirmDelete() {
        
        fetch(`/api/products/${this.product.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ confirm_delete: true }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error('Failed to delete product');
            }
            return response.json();
          })
          .then((data) => {
            
            console.log(data);
            alert('Product deleted successfully');
          })
          .catch((error) => {
            
            console.error(error);
          });
      },
    },
}
</script>