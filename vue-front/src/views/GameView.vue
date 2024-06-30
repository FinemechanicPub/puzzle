<script setup>
    import { ref, watch } from 'vue'
    import getGame from '@/api/game'
    import Board from '@/components/Board.vue';

    const props = defineProps({
        id: String
    })

    const loading = ref(false)
    const error = ref(null)
    const game = ref(null)

    const board = ref(null)
    const piece = ref({
        id: 1,
        rotation: 3,
        color: 0x750f83,
        points: [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]]
    })

    // watch the params of the route to fetch the data again
    watch(() => props.id, fetchData, { immediate: true })

    async function fetchData(id) {
        error.value = game.value = null
        loading.value = true
        
        try {
            game.value = await getGame(parseInt(id))  
        } catch (err) {
            error.value = err.toString()
        } finally {
            loading.value = false
        }
    }
</script>

<template>
    <h2>Game #{{ id }}</h2>
    <main>
        <div v-if="loading" class="loading">Загружается...</div>
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="game" class="content">
            <Board :width="game.width" :height="game.height" :piece="piece" ref="board"/>
            <button @click="board.reset">Reset</button>

        </div>
        
    </main>
</template>