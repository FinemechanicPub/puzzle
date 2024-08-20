<script setup>
  import {ref, watch } from 'vue';

  import divmod from '@/utils/divmod';

  const props = defineProps({
    width: Number,
    height: Number,
    cellSize: Number,
    installed_pieces: Array
  })
  const emit = defineEmits(['install', 'remove'])

  const cell_width = `${props.cellSize}px`
  const board = ref(null)
  const grid = ref(Array(props.height).fill().map(()=>Array(props.width).fill(0xffffff)))

  function get_board_rect(){
    return board.value.getBoundingClientRect()
  }
  
  defineExpose({ get_board_rect })


  watch(props.installed_pieces, render_board, { immediate: true, deep: true })

  function render_board(){
    console.log(`render board`)
    grid.value = Array(props.height).fill().map(()=>Array(props.width).fill(0xffffff))
    for (const installedPiece of props.installed_pieces){      
      render_piece(installedPiece.index, installedPiece.rotation.points, installedPiece.piece.color)
    }
  }

  function render_piece(index, points, color){
    console.log(`render at cell #${index}`)
    const [row, column] = divmod(index, props.width)
    for (const [y, x] of points){
      grid.value[row + y][column + x] = color
    }
  }

  function onDrop(evt, index){
      console.log('drop piece on cell #', index)
      const raw_data = evt.dataTransfer.getData('piece_data')
      if (!raw_data){
        console.log("no drop data")
        return
      }
      const piece_data = JSON.parse(raw_data)
      const cellRect = evt.target.getBoundingClientRect()
      const amendX = Math.floor((evt.clientX - cellRect.left - piece_data.offsetX) / props.cellSize)
      const amendY = Math.floor((evt.clientY - cellRect.top - piece_data.offsetY) / props.cellSize)
      const corrected_index = index + piece_data.dx + amendX + (piece_data.dy + amendY)*props.width
      emit('install', piece_data.pieceId, piece_data.rotationId, corrected_index)
  }

  function onClick(evt, index){
    emit('remove', index)
  }

</script>

<style scoped>
  .grid {
    display: grid;
    grid-template-columns: repeat(v-bind("props.width"), 1fr);
    border: 1px solid gray;
    overflow: hidden;
  }
  .square {
    aspect-ratio: 1/ 1;
    width: var(--cell-width);
    border: 1px solid gray;
  }
  .centered {
    margin: auto;
  }
</style>

<template>
  <div ref="board" class="board grid centered width-fit-content" >
    <div class="square" @click="onClick($event, index)" @drop="onDrop($event, index)" @dragover.prevent @dragenter.prevent v-for="(cell, index) in grid.flat()" :key="index" v-bind:style="{'background-color': `#${cell.toString(16)}`}"></div>
  </div>
</template>