<script setup>
    import { onMounted, ref } from 'vue';
    import { mainListMenu } from '@/api/generated';

    const menus = ref(null)

    async function fetchMenu(){
        menus.value = null
        try {
            menus.value = await mainListMenu()
        } catch (err){
            console.log("fetching menus caused the error: ", err.toString())
        }
    }
    onMounted(() => fetchMenu())
</script>

<style scoped>
    header{
    display: flex;
    align-items: center;
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
    <nav v-if="menus">
      <ul>
        <li v-for="menu of menus" :key="menu.id">
            <RouterLink :to="{name: 'main', query: menu.query}">{{ menu.title }}</RouterLink>
        </li> 
      </ul>
    </nav>
  </header>
</template>