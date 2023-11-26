<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <h1>HIDRO</h1>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/home2">Home 2</RouterLink>
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
</style>
