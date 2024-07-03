<script setup>
  import { computed, ref } from 'vue'

  import divmod from '@/utils/divmod'

  const props = defineProps({
    piece: Object
  })
  const emit = defineEmits(['cell-click'])

  const hovering = ref(false)

  const rotationIndex = ref(0)
  const rotation = computed(() => props.piece.rotations[rotationIndex.value]) 
  const points = computed(() => rotation.value.points)
  const color = computed(() => props.piece.color)
  const colorString =  computed(() => `#${props.piece.color.toString(16)}`)
  const maxX = computed(() => Math.max(...points.value.map((point) => point[1])))
  const minX = computed(() => Math.min(...points.value.map((point) => point[1])))
  const maxY = computed(() => Math.max(...points.value.map((point) => point[0])))
  const grid = computed(make_grid)
  const width = computed(() => maxX.value - minX.value + 1)
  const canFlip = computed(() => props.piece.rotations.length > 4)
  const canRotate = computed(() => props.piece.rotations.length > 1)

  function make_grid(){
    const grid = Array(maxY.value + 1).fill().map(()=>Array(maxX.value - minX.value + 1).fill(false))
    for (const [y, x] of points.value){
      grid[y][x - minX.value] = true
    }
    return grid
  }
  const mouse_index = ref(null)

  function piece_click(cell, index){
    console.log(`clicked cell, which is '${cell}'`)
    if (cell){
      const dy = Math.floor(index / width.value)
      const dx = index % width.value
      emit('cell-click', dy, dx)
    }
  }

  function on_mouse_down(index){
    console.log(`mouse down in cell #${index}`)
    mouse_index.value = index
  }

  function startDrag(evt){
      console.log('dragging piece')
      const [dy, dx] = divmod(mouse_index.value, width.value)
      const piece_data = {
        dy: -dy,
        dx: -dx - minX.value,
        piece: {color: color.value, points: points.value}
      }
      evt.dataTransfer.dropEffect = 'move'
      evt.dataTransfer.effectAllowed = 'move'
      evt.dataTransfer.setData('piece_data', JSON.stringify(piece_data))
  }

  function rotate(direction){
    if (props.piece.rotations.length > 4){
      const [half, index] = divmod(rotationIndex.value, 4)
      rotationIndex.value = 4 * half + (index + 4 + direction) % 4
    } else {
      rotationIndex.value = (props.piece.rotations.length + rotationIndex.value + direction) % props.piece.rotations.length
    }
  }

  function flip(){
    const cycleLength = props.piece.rotations.length > 2 ? Math.floor(props.piece.rotations.length / 2) : 0
    rotationIndex.value = (rotationIndex.value + cycleLength) % props.piece.rotations.length
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
    width: 18px;
    display: flex;
    /* justify-content: center; */
    margin: 1px;
  }
  .colored {
    background-color: v-bind(colorString);
  }
  .placeholder{
    display: flex;
    flex-direction: row;
  }
  .piece-area{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 100px;
    /* background: gray; */
  }
  .invisible {
    visibility: hidden;
  }
  .centered {
    text-align: center;
  }
</style>

<template>
  <div @mouseenter="hovering=true" @mouseleave="hovering=false">
    <div class="placeholder" >
      <div :class="{invisible: !(hovering && canRotate)}" @click="rotate(1)">L</div>
      <div class="piece-area">
        <div class="piece grid" draggable="true" @dragstart="startDrag($event)">
          <div class="square" :class="{ colored: cell }" @mousedown="on_mouse_down(index)" @click="piece_click(cell, index)" v-for="(cell, index) in grid.flat()" :key="index"></div>
        </div>
      </div>
      <div :class="{invisible: !(hovering && canRotate)}" @click="rotate(-1)">R</div>
    </div>
    <div>
      <div class="centered" :class="{invisible: !(hovering && canFlip)}" @click="flip">F</div>
    </div>
  </div>
</template>