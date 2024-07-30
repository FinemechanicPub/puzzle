<script setup>
    import { computed, ref, watch, watchEffect } from 'vue';
    import divmod from '@/utils/divmod';
    import counter from '@/utils/counter'
    import Board from '@/components/Board.vue';
    import PiecePalette from '@/components/PiecePalette.vue'
    import HintBox from '@/components/HintBox.vue'
    import { gamesGetGame } from '@/api/generated'
    import { ApiError } from '@/api/generated';

    const props = defineProps({
        id: String
    })

    const loading = ref(false)
    const error = ref(null)
    const game = ref(null)
    const storageKey = computed(() => `puzzle${game.value.id}`)
    const installedPieces = ref([])
    const installedCount = computed(() => counter(installedPieces.value.map((item) => item.piece)))
    const availablePieces = computed(
        () => game.value.pieces.filter((piece) => piece.count - (installedCount.value[piece.id] || 0) > 0)
    )

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
    watchEffect(saveGame)

    function saveGame(){
        if (installedPieces.value.length){
            console.log("save game")
            localStorage.setItem(
                storageKey.value,
                JSON.stringify(installedPieces.value.map((item) => [item.piece.id, item.rotation.id, item.index]))
            )
        }
    }

    function loadGame(){
        console.log("load game")
        const savedGame = localStorage.getItem(storageKey.value)
        if (savedGame){
            for (const item of JSON.parse(savedGame)){
                handleInstall(...item)
            }
        }
    }

    async function fetchData(id) {
        error.value = game.value = null
        loading.value = true
        
        try {
            game.value = await gamesGetGame({
                gameId: parseInt(id)
            })
            loadGame()
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
        const piece = game.value.pieces.find((piece) => piece.id == id)
        const rotation = piece.rotations.find((rotation) => rotation.id == rotationId)
        console.log('rotation found: ', rotation.id)
        if (hasCollision(index, rotation.points)){
            return
        }
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
        }
    }


</script>

<style scoped>
    .content {
        width: 90%;
        margin: auto;
        padding: 2ch;
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
        margin: 1ch auto;
        width: -moz-fit-content;
        width: fit-content;
    }
    .card-green{
        border-radius: 10px;
        padding: 20px;
        margin: 1ch auto;
        width: -moz-fit-content;
        width: fit-content;
        font-weight: bolder;
        color: slateblue;
        background: mediumaquamarine;
        border: 2px solid lightseagreen;
        text-align: center; 
    }
    .button{
        margin: 1ch auto;
        width: -moz-fit-content;
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
    <h2 v-if="loading" class="loading">Загрузка данных...</h2>
    <div v-if="error" class="error">
        <h3>Ошибка подключения к серверу</h3>
        <p>{{ error }}</p>
    </div>
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