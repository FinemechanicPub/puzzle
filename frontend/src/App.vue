<script setup>

</script>

<style src="vue3-tour/dist/vue3-tour.css">
</style>

<style scoped>
header{
  display: flex;
  align-items: baseline;
  justify-content: left;
}
nav {
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  padding: 1rem;
  width: 100%;
}
nav ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: space-around;
}
nav ul li a {
  color: white;
  text-decoration: none;
  font-size: 1.1rem;
  transition: color 0.3s ease;
}
nav ul li a:hover {
  color: #ffd700;
}
nav ul li a.active {
  color: #ffd700;
  font-weight: bold;
}
</style>

<template>
  <header>
    <h1>
      <RouterLink to="/" class="logo">Плитки</RouterLink>
    </h1>
    <nav>
      <ul>
        <li><RouterLink :to="{name: 'main', query: {height: 5, width: 5}}">5x5</RouterLink></li>
        <li><RouterLink :to="{name: 'main', query: {height: 8, width: 5}}">8x5</RouterLink></li> 
      </ul>
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
</template>
