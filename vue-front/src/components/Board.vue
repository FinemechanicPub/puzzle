<script setup>
  import { ref, watch } from 'vue';

  import divmod from '@/utils/divmod';

  const props = defineProps({
    width: Number,
    height: Number,
    installed_pieces: Array
  })

  const emit = defineEmits(['install', 'remove'])

  const grid = ref(Array(props.height).fill().map(()=>Array(props.width).fill(0xffffff)))

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
      const piece_data = JSON.parse(evt.dataTransfer.getData('piece_data'))
      console.log(piece_data)
      const corrected_index = index + piece_data.dx + piece_data.dy*props.width
      emit('install', piece_data.pieceId, piece_data.rotationId, corrected_index)
  }

  function onClick(evt, index){
    emit('remove', index)
  }

</script>

<style scoped>
  .grid {
    display: grid;
    grid-template-columns: repeat(v-bind(width), 1fr);
    border: 1px solid gray;
  }
  .square {
    aspect-ratio: 1/ 1;
    width: 20px;
    display: flex;
    justify-content: center;
    /* padding: 1%; */
    border: 1px solid gray;
    color: #8252d4;
  }
  .centered {
    width: fit-content;
    margin: auto;
  }
</style>

<template>
  <div class="board grid centered" >
    <div class="square" @click="onClick($event, index)"  @drop="onDrop($event, index)" @dragover.prevent @dragenter.prevent v-for="(cell, index) in grid.flat()" :key="index" v-bind:style="{'background-color': `#${cell.toString(16)}`}"></div>
  </div>
</template>