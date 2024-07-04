<script setup>
    import { computed, ref, watch } from 'vue';
    import getGame from '@/api/game';
    import getHint from '@/api/hint';
    import divmod from '@/utils/divmod';
    import Board from '@/components/Board.vue';
    import PiecePalette from '@/components/PiecePalette.vue'

    const props = defineProps({
        id: String
    })

    const loading = ref(false)
    const error = ref(null)
    const game = ref({
        width: -1,
        height: -1,
    })
    const gamePieces = ref([])
    const gameError = ref(null)
    const availablePieces = computed(() => gamePieces.value.filter((item) => item.count > 0).map((item) => item.piece))
    const installed_pieces = ref([])

    const occupiedCells = computed(
        () => installed_pieces.value.reduce(
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

    async function fetchHint(){
        gameError.value = null
        try{
            const hint = await getHint(props.id, installed_pieces.value.map((item)=> ({piece_id: item.piece.id, rotation_id: item.rotation.id, position: item.index})))
            console.log("hint ", hint)
            handleInstall(hint.piece_id, hint.rotation_id, hint.position)
        } catch (err) {
            gameError.value = err.toString()
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
        installed_pieces.value.push({
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
    .center{
        display: flex;
        justify-content: center;
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
    .error{
        border-radius: 10px;
        background: papayawhip;
        border: 2px solid peachpuff;
        padding: 20px;
        width: 200px;
        margin: 1ch auto;
    }
    .card{
        border-radius: 10px;
        padding: 20px;
        margin: 1ch auto;
    }
    .card-green{
        background: palegreen;
        border: 2px solid lawngreen;
    }
    .button{
        margin-top: 1ch;
    }
</style>

<template>
    <div>
        <h2>Game #{{ id }}</h2>
        <div>
            <div v-if="loading" class="loading">Загружается...</div>
            <div v-if="error" class="error">{{ error }}</div>
            <div v-if="game" class="content flex-center-content one-column">
                <div v-if="gameComplete" class="card card-green">
                    Победа!
                </div>
                <div>
                    <Board @install="handleInstall" @remove="handleRemove" :width="game.width" :height="game.height" :installed_pieces="installed_pieces" />
                </div>
                <div v-if="gameError" class="error">
                    <div>
                        {{ gameError }}
                    </div>
                    <button class="transparent-button" @click="gameError=null">[закрыть]</button>
                </div>
                <div class="flex-center-content">
                    <button class="button" :disabled="gameComplete"  @click="fetchHint">Показать подсказку</button>
                </div>
                <PiecePalette :availablePieces="availablePieces" />
            </div>
            
        </div>

    </div>
</template>