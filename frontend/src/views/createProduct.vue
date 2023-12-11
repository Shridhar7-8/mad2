<template>
<div class="create-section-container">
      <h1>Create Section</h1>
      <form @submit.prevent="createSection">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="section.name" required>
        </div>
        <div class="form-group">
          <label for="section_type">Section Type:</label>
          <input type="text" id="section_type" v-model="section.section_type" required>
        </div>
        <button type="submit">Create Section</button>
      </form>
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
    };
  },
  methods: {
    createSection() {
      const requestData = {
        name: this.section.name,
        section_type: this.section.section_type,
      };

      fetch('http://127.0.0.1:5000/api/sections', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to create section');
          }
          return response.json();
        })
        .then(data => {
          console.log('Section created:', data);
          alert('Section created successfully');

          this.section.name = '';
          this.section.section_type = '';
        })
        .catch(error => {
          console.error(error);
          alert('Failed to create section. Please try again later.');
        });
    },
  },
}
</script>