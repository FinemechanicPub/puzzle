<script setup>
    import { onMounted, ref } from 'vue';
    import GameCarousel from '@/components/GameCarousel.vue'
    import { mainPageSuggestion } from '@/api/generated'
    import { ApiError } from '@/api/generated/core/ApiError'

    const error = ref(null)
    const loading = ref(false)
    const games = ref([])

    onMounted(fetchData)

    async function fetchData() {
        error.value = games.value = null
        loading.value = true
        
        try {
            games.value = await mainPageSuggestion()
        } catch (err) {
            if (err instanceof ApiError){
                error.value = `${err.status} - ${err.statusText}`
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
    flex-direction: column;
    flex-wrap: wrap;
    gap: 5%;
    justify-content: center;
    margin: 5ch 5%;
    min-width: 240px;
}

</style>

<template>
    <GameCarousel v-if="games" :games="games"/>
    <div v-if="error">
        Произошла ошибка: {{ error }}
    </div>
</template>