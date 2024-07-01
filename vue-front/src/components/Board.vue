<script setup>
  import { ref, watch } from 'vue';

  import divmod from '@/utils/divmod';

  const props = defineProps({
    width: Number,
    height: Number,
    piece: Object
  })  
  const grid = ref(Array(props.height).fill().map(()=>Array(props.width).fill(0xffffff)))
  // const piece = ref([[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]])
  const history = ref([])
  const redo = ref([])

  watch(history, render_board, { immediate: true, deep: true })

  function render_board(){
    console.log(`render board`)
    grid.value = Array(props.height).fill().map(()=>Array(props.width).fill(0xffffff))
    for (const [position, piece, flat_points] of history.value){
      render_piece(position, piece.points, piece.color)
    }
  }

  function render_piece(index, points, color){
    console.log(`render at cell #${index}`)
    const [row, column] = divmod(index, props.width)
    for (const [y, x] of points){
      grid.value[row + y][column + x] = color
    }
  }

  function collision(pieces, points, position, flat_points){
    const [row, column] = divmod(position, props.width)
    for (const [y, x] of points){
      if (
        column + x >= props.width 
        || column + x < 0 
        || row + y >= props.height 
        || row + y < 0
      ) {
        console.log('collision')
        return true
      }
    }
    const board_pieces = new Set(flat_points);
    for (const [_, __, history_flat] of pieces){
      if (!board_pieces.isDisjointFrom(new Set(history_flat))){
        console.log('collision with another piece')
        return true
      }
      for (const i of history_flat){
        board_pieces.add(i)
      }
    }
    return false
  }

  function flatten(position, points){
    const flat_points = []
    for (const [y, x] of points){
      flat_points.push(position + x + y * props.width)
    }
    return flat_points
  }

  function place_piece(index, piece){
    console.log(`place_piece to cell #${index}`)
    if (piece){
      const flat_points = flatten(index, piece.points)
      if (!collision(history.value, piece.points, index, flat_points)){
        history.value.push([index, piece, flat_points])
        redo.value = []
      }
    }
  }

  function remove_piece(){
    if (history.value.length){
      redo.value.push(history.value.pop())
    }
  }

  function restore_piece(){
    if (redo.value.length){
      history.value.push(redo.value.pop())
    }
  }

  function reset(){
    console.log("reset")
    while (history.value.length){
      remove_piece()
    }
  }

  function onDrop(evt, index){
      console.log('drop piece on cell #', index)
      const piece_data = JSON.parse(evt.dataTransfer.getData('piece_data'))
      const corrected_index = index + piece_data.dx + piece_data.dy*props.width
      place_piece(corrected_index, piece_data.piece)
  }

  defineExpose({
    reset
  })
</script>

<style scoped>
  .grid {
    display: grid;
    grid-template-columns: repeat(v-bind(width), 1fr);
    border: 1px solid #19b440;
  }
  .square {
    aspect-ratio: 1/ 1;
    width: 20px;
    display: flex;
    justify-content: center;
    /* padding: 1%; */
    border: 1px solid #19b440;
    color: #8252d4;
  }
  .centered {
    width: fit-content;
    margin: auto;
  }
</style>

<template>
  <div class="board grid centered" >
    <div class="square" @click="place_piece(index, props.piece)" @drop="onDrop($event, index)" @dragover.prevent @dragenter.prevent v-for="(cell, index) in grid.flat()" :key="index" v-bind:style="{'background-color': `#${cell.toString(16)}`}"></div>
  </div>
  <div class="centered">
    <button :disabled="history.length == 0"  @click="remove_piece">Убрать ({{ history.length }})</button>
    <button :disabled="history.length == 0"  @click="reset">Сбросить</button>
    <button :disabled="redo.length == 0" @click="restore_piece">Вернуть ({{ redo.length }})</button>
  </div>
</template>