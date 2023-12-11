<template>
<div class="login-container">
      <h2>Admin Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <button type="submit">Login</button>
      </form>
      <div v-if="showMessage" class="alert alert-danger">{{ errorMsg }}</div>
      <div class="mt-3">
        <router-link to="/register">Don't have an account? Register here</router-link>
      </div>
    </div>
</template>
<script>
export default{
    data() {
    return {
      showLoginForm: true,
      showMessage: false,
      errorMsg: "",
      username: "",
      password: "",
    };
  },
  methods: {
    login() {
      const payload = {
        username: this.username,
        password: this.password,
      };

      fetch("http://127.0.0.1:5000/login?include_auth_token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Invalid Username/password");
          }
        })
        .then((data) => {
          // Store the authentication token in local storage
          localStorage.setItem('auth_token', data.response.user.authentication_token);

          // Redirect to the home page
          this.$router.push('/');
        })
        .catch((error) => {
          this.showError("Invalid username or password.");
          console.error(error);
        });
    },
    showError(message) {
      this.showMessage = true;
      this.errorMsg = message;
      setTimeout(() => {
        this.showMessage = false;
      }, 3000);
    },
  },
}
</script>