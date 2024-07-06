<script setup>
    import { computed, ref, watch } from 'vue';
    import getGame from '@/api/game';
    import divmod from '@/utils/divmod';
    import Board from '@/components/Board.vue';
    import PiecePalette from '@/components/PiecePalette.vue'
    import HintBox from '@/components/HintBox.vue'

    const props = defineProps({
        id: String
    })

    const loading = ref(false)
    const error = ref(null)
    const game = ref(null)
    const gamePieces = ref([])
    const availablePieces = computed(() => gamePieces.value.filter((item) => item.count > 0).map((item) => item.piece))
    const installedPieces = ref([])

    const occupiedCells = computed(
        () => installedPieces.value.reduce(
        (prev, item) => prev.concat(item.rotation.points.map(
            (point) => [item.index + point[0]*game.value.width + point[1], item.piece]
        )), []
        )
    )
    const occupiedPositions = computed(() => occupiedCells.value.map((item) => item[0]))
    const gameComplete = computed(() => occupiedPositions.value.length == game.value.width * game.value.height)

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
            id: game_data.id,
            title: game_data.title,
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
      if (occupiedPositions.value.includes(p)){
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
        installedPieces.value.push({
            piece: piece,
            rotation: rotation,
            index: index
        })
    }

    function handleRemove(position){
        console.log('handleRemove ', position)
        if (occupiedPositions.value.length == 0){
            return
        }
        const cell_data = occupiedCells.value.find((item) => item[0] == position)
        if (cell_data){
            const piece = cell_data[1]
            const index = installedPieces.value.findIndex((item) => item.piece == piece)
            installedPieces.value.splice(index, 1)
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
    .center{
        display: flex;
        justify-content: center;
    }
    .piece-palette{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    .piece-frame{
        margin: 5px;
    }
    .error{
        border-radius: 10px;
        background: papayawhip;
        border: 2px solid peachpuff;
        padding: 20px;
        width: 200px;
        margin: 1ch auto;
    }
    .card-green{
        border-radius: 10px;
        padding: 20px;
        margin: 1ch auto;
        width: fit-content;
        font-weight: bolder;
        color: slateblue;
        background: mediumaquamarine;
        border: 2px solid lightseagreen;
        text-align: center; 
    }
    .button{
        margin: 1ch auto;
        width: fit-content;
    }
    .hint-box{
        display: inline-flex;
        margin: auto;
        gap: 1ch;
    }
    .big{
        font-size: larger;
    }
</style>

<template>
    <div v-if="loading" class="loading">Загружается...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="game" class="content flex-center-content one-column">
        <h2>{{ game.title }}</h2>
        <div v-auto-animate>
            <div :key=1 v-if="gameComplete" class="card-green">
                <p class="big">🏅</p>
                <p>Доска заполнена!</p>
            </div>
        </div>
        <Board @install="handleInstall" @remove="handleRemove" :width="game.width" :height="game.height" :installed_pieces="installedPieces" />
        <HintBox @hint="hint => handleInstall(...hint)" :gameId="game.id" :installedPices="installedPieces" />
        <PiecePalette :availablePieces="availablePieces" />            
    </div>
</template>