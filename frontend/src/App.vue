<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script setup>
// No logic needed here
</script>

<style>
.app-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  font-family: system-ui, sans-serif;
}
h1 {
  text-align: center;
  color: #2c3e50;
}
input, button {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border-radius: 6px;
  border: 1px solid #ddd;
  font-size: 16px;
}
button {
  background: #3498db;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background: #2980b9;
}
.error {
  color: #e74c3c;
  text-align: center;
}
.success {
  color: #27ae60;
  text-align: center;
}
</style>