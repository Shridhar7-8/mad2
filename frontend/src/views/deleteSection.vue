<template>
<div class="delete-section-container">
        <h2>Delete Section</h2>
        <p>Are you sure you want to delete this section? This will also delete all the products inside the section.</p>
        <form @submit.prevent="confirmDelete">
          <input type="hidden" name="confirm_delete" value="true">
          <button type="submit" class="btn btn-danger">Confirm Deletion</button>
        </form>
        <router-link to="/admindashboard" class="btn btn-secondary">Cancel</router-link>
      </div>
</template>
<script>
export default{
    methods: {
      confirmDelete() {
        
        fetch(`/api/sections/${this.$route.params.sectionId}`, {
           method: 'DELETE',
         })
           .then((response) => {
             if (!response.ok) {
               throw new Error('Failed to delete section');
             }
             return response.json();
           })
           .then((data) => {
              
             console.log(data);
             alert('Section deleted successfully');
           })
           .catch((error) => {
             
             console.error(error);
           });
        
        
        console.log('Section deleted');
        alert('Section deleted successfully');
        this.$router.push('/admindashboard');
      },
    },
}
</script>