<template>
    <div>
      <div>
        <div v-if="messages.length > 0">
          <div v-for="message in messages" :key="message">
            <p>{{ message }}</p>
          </div>
        </div>
      </div>

      <h3>Sections:</h3>
      <router-link to="/create_section" class="btn btn-primary">Create Section</router-link>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="section in sections" :key="section.id">
            <td>{{ section.name }}</td>
            <td>
              <router-link :to="'/edit_section/' + section.id" tag="a" class="btn btn-secondary">Edit</router-link>
              <router-link :to="'/delete_section/' + section.id" tag="a" class="btn btn-danger">Remove</router-link>
              <router-link :to="'/view_section/' + section.id" tag="a" class="btn btn-info">View Products</router-link>
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
      messages: [], 
      sections: [], 
    };
  },
  created() {
    fetch('/api/sections')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      this.sections = data;
    })
    .catch(error => {
      console.error('Error fetching sections:', error);
    });
  },
}
</script>