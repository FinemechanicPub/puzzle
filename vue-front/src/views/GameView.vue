<script setup>
    import { computed, ref, watch } from 'vue';
    import getGame from '@/api/game';
    import divmod from '@/utils/divmod';
    import Board from '@/components/Board.vue';
    import Piece from '@/components/Piece.vue';

    const props = defineProps({
        id: String
    })

    const loading = ref(false)
    const error = ref(null)
    const game = ref(null)
    const gamePieces = ref([])
    const availablePieces = computed(() => gamePieces.value.filter((item) => item.count > 0).map((item) => item.piece))
    const installed_pieces = ref([])

    const occupiedCells = computed(
        () => installed_pieces.value.reduce(
        (prev, item) => prev.concat(item.rotation.points.map(
            (point) => [item.index + point[0]*game.value.width + point[1], item.piece]
        )), []
        )
    )
    const occupiedPoints = computed(() => occupiedCells.value.map((item) => item[0]))

    const board = ref(null)

    // watch the params of the route to fetch the data again
    watch(() => props.id, fetchData, { immediate: true })

    async function fetchData(id) {
        error.value = game.value = null
        loading.value = true
        
        try {
            const data = await getGame(parseInt(id))
            setupGame(data)
        } catch (err) {
            error.value = err.toString()
        } finally {
            loading.value = false
        }
    }

    function setupGame(game_data){
        gamePieces.value = game_data.pieces.map((item) => ({count: 1, piece: item}))
        game.value = {
            width: game_data.width,
            height: game_data.height
        }
    }

    function hasCollision(position, points){
    const [row, column] = divmod(position, game.value.width)
    for (const [y, x] of points){
      if (
        column + x >= game.value.width 
        || column + x < 0 
        || row + y >= game.value.height 
        || row + y < 0
      ) {
        console.log('collision')
        return true
      }
    }
    for (const [y, x] of points){
      const p = position + y*game.value.width + x
      if (occupiedPoints.value.includes(p)){
        console.log('collision with another piece')
        return true
      }
    }
    return false
  }

    function handleInstall(id, rotationId, index){
        console.log('handleInstall', id, rotationId)
        const item = gamePieces.value.find((item) => item.piece.id == id)
        const piece = item.piece
        const rotation = piece.rotations.find((rotation) => rotation.id == rotationId)
        console.log('rotation found: ', rotation.id)
        if (hasCollision(index, rotation.points)){
            return
        }
        item.count--;
        installed_pieces.value.push({
            piece: piece,
            rotation: rotation,
            index: index
        })
    }

    function handleRemove(position){
        console.log('handleRemove ', position)
        const [_, piece] = occupiedCells.value.find((item) => item[0] == position)
        console.log('piece to remove: ', piece)
        if (piece){
            const index = installed_pieces.value.findIndex((item) => item.piece == piece)
            installed_pieces.value.splice(index, 1)
            const gameItem = gamePieces.value.find((item) => item.piece == piece)
            gameItem.count++
        }
    }
</script>

<style scoped>
    .content {
        width: 90%;
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
                <Board @install="handleInstall" @remove="handleRemove" :width="game.width" :height="game.height" :installed_pieces="installed_pieces" ref="board"/>
            </div>
            <div class="piece-palette" v-auto-animate>
                <div class="piece-frame" :key="piece.id" v-for="piece in availablePieces">
                    <Piece :piece="piece"/>
                </div>
            </div>
        </div>
        
    </main>
</template>