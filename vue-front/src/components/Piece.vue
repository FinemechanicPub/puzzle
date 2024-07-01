<script setup>
import { ref, watch } from 'vue'
  const props = defineProps({
    piece: Object
  })
  const emit = defineEmits(['cell-click'])

  const piece = props.piece
  const max_x = Math.max(...piece.points.map((point) => point[1]))
  const min_x = Math.min(...piece.points.map((point) => point[1]))
  const max_y = Math.max(...piece.points.map((point) => point[0]))
  const height = max_y + 1
  const width = max_x - min_x + 1
  const grid = Array(height).fill().map(()=>Array(width).fill(false))
  for (const [y, x] of piece.points){
    grid[y][x - min_x] = true
  }
  const color = `#${piece.color.toString(16)}`

  console.log(min_x, max_x, max_y)

  function piece_click(cell){
    console.log(`clicked cell, which is '${cell}'`)
    if (cell){
      emit('cell-click')
    }
  }
</script>

<style scoped>
  .grid {
    display: grid;
    grid-template-columns: repeat(v-bind(width), 1fr);
    width: fit-content;
  }
  .square {
    aspect-ratio: 1/ 1;
    width: 20px;
    display: flex;
    justify-content: center;
    margin: 1px;
  }
  .colored {
    background-color: v-bind(color)
  }
</style>

<template>
  <div class="piece grid" >
    <div class="square" :class="{ colored: cell }" @click="piece_click(cell)" v-for="(cell, index) in grid.flat()" :key="index"></div>
  </div>
</template>