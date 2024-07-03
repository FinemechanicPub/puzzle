<script setup>
    import { ref, watch } from 'vue';
    import getGame from '@/api/game';
    import Board from '@/components/Board.vue';
    import Piece from '@/components/Piece.vue';

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

    function select_piece(piece_data, dy, dx){
        console.log("piece clicked")
        piece.value = {
            id: piece_data.id,
            color: piece_data.color,
            points: piece_data.rotations[0].points
        }
    }
</script>

<style scoped>
    .content {
        width: 60%;
        margin: auto;
    }
    .piece-palette{
        /* display: grid; */
        display: flex;
        flex-wrap: wrap;
        /* width: fit-content; */
        /* grid-template-columns: repeat(3, 1fr); */
        /* grid-template-columns: fit-content(40%);  */
    }
    .piece-frame{
        margin: 5px;
    }
</style>

<template>
    <h2>Game #{{ id }}</h2>
    <main>
        <div v-if="loading" class="loading">Загружается...</div>
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="game" class="content">
            <div>
                <Board :width="game.width" :height="game.height" :piece="piece" ref="board"/>
            </div>
            <div class="piece-palette">
                <div class="piece-frame" :key="piece.id" v-for="piece in game.pieces">
                    <Piece  @cell-click="(dy, dx) => select_piece(piece, dy, dx)" :piece="piece"/>
                </div>
            </div>
        </div>
        
    </main>
</template>