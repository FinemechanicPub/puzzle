<script setup>
  import { ref, watch } from 'vue'
  const props = defineProps({
    width: Number,
    height: Number,
    piece: Object
  })  
  const grid = ref(Array(props.height).fill().map(()=>Array(props.width).fill(0xffffff)))
  // const piece = ref([[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]])
  const history = ref([])

  watch(() => history, render_board, { immediate: true, deep: true })

  function render_board(){
    console.log(`render board`)
    grid.value = Array(props.height).fill().map(()=>Array(props.width).fill(0xffffff))
    console.log(history.value)
    for (const [position, piece, flat_points] of history.value){
      render_piece(position, piece.points, piece.color)
    }
  }

  function render_piece(index, points, color){
    console.log(`render ${index}`)
    const [row, column] = divmod(index, props.width)
    console.log(row, column)
    for (const [y, x] of points){
      grid.value[row + y][column + x] = color
    }
  }

  function divmod(divisor, divident){
    const quotinet = Math.floor(divisor / divident)
    const remainder = divisor % divident
    return [quotinet, remainder]
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

  function place_piece(index){
    console.log(`click ${index}`)
    if (props.piece){
      const flat_points = flatten(index, props.piece.points)
      if (!collision(history.value, props.piece.points, index, flat_points)){
        history.value.push([index, props.piece, flat_points])
      }
    }
  }

  function reset(){
    console.log("reset")
    history.value =[]
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
    width: fit-content;
    margin: auto;
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
</style>

<template>
  <p>{{ props.width }} x {{ props.height }}</p>
  <div class="board grid" >
    <div class="square" @click="place_piece(index)" v-for="(cell, index) in grid.flat()" :key="index" v-bind:style="{'background-color': `#${cell.toString(16)}`}"></div>
  </div>
</template>