<script setup>
    import { onMounted, ref } from 'vue';
    import getGames from '@/api/cover.js'
    import GameCard from '@/components/GameCard.vue';

    const error = ref(null)
    const loading = ref(false)
    const games = ref([])

    onMounted(fetchData)
    

    async function fetchData() {
        error.value = games.value = null
        loading.value = true
        
        try {
            console.log("start fetch")
            games.value = await getGames()
            console.log("start fetch complete")
            console.log(games.value)
        } catch (err) {
            console.log("fetch error")
            if (err instanceof TypeError){
                error.value = err.message
            } else {
                error.value = err.toString()
            }
        } finally {
            loading.value = false
        }
    }
</script>

<style scoped>
.game-roulette{
    display: flex;
    flex-direction: row;
    gap: 5%;
    justify-content: center;
    align-content: baseline;
    margin: 5ch auto;
}

</style>

<template>
    <div v-if="games" class="game-roulette">
        <div :key="game.id" v-for="game in games">
            <RouterLink :to="{name: 'game', params: {id: game.id}}">
                <GameCard :game="game" />
            </RouterLink>
        </div>
    </div>
</template>