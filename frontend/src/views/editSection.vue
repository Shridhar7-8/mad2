<template>
<div class="edit-section-container">
      <h1>Edit Section</h1>
      <form @submit.prevent="updateSection">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="section.name" required>
        </div>
        <div class="form-group">
          <label for="section_type">Section Type:</label>
          <input type="text" id="section_type" v-model="section.section_type">
        </div>
        <button type="submit">Update Section</button>
      </form>
    </div>
</template>
<script>
export default{
    data() {
    return {
      section: {
        id: null,
        name: '',
        section_type: '',
      },
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
  },
  methods: {
    updateSection() {
      const sectionId = parseInt(this.$route.params.sectionId);
      fetch(`/api/sections/${sectionId}`, {
        method: 'PUT', 
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.section),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Failed to update section');
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert('Section updated successfully');
          
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
}
</script>