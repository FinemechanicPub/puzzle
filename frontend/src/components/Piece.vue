<script setup>
  import { computed, ref } from 'vue'

  import divmod from '@/utils/divmod'

  const props = defineProps({
    piece: Object
  })

  const hovering = ref(false)

  const rotationIndex = ref(0)
  const rotation = computed(() => props.piece.rotations[rotationIndex.value]) 
  const points = computed(() => rotation.value.points)
  const colorString =  computed(() => `#${props.piece.color.toString(16)}`)
  const maxX = computed(() => Math.max(...points.value.map((point) => point[1])))
  const minX = computed(() => Math.min(...points.value.map((point) => point[1])))
  const maxY = computed(() => Math.max(...points.value.map((point) => point[0])))
  const diameter = computed(() => (1 + Math.max(maxX.value - minX.value, maxY.value)))
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
        pieceId: props.piece.id,
        rotationId: rotation.value.id
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
    width: -moz-fit-content;
    width: fit-content;
  }
  .piece-cell {
    aspect-ratio: 1/ 1;
    width: 18px;
    display: flex;
    /* justify-content: center; */
    margin: 1px;
  }
  .colored {
    background-color: v-bind(colorString);
  }
  .container-row{
    display: flex;
    flex-direction: row;
  }
  .piece-box{
    display: flex;
    align-items: center;
    justify-content: center;
    width: v-bind(18*diameter + "px");
    height: 100px;
  }
  .invisible {
    visibility: hidden;
  }
  .centered {
    text-align: center;
  }
  .cursor-pointer{
    cursor: pointer
  }
  .flex-center-content{
    display: flex;
    justify-content: center;
  }

</style>

<template>
  <div class="hover" @mouseenter="hovering=true" @mouseleave="hovering=false">
    <div class="container-row" >
      <button class="transparent-button" :class="{invisible: !(hovering && canRotate)}" @click="rotate(1)">⤹</button>
      <div class="piece-box">
        <div class="piece grid cursor-pointer" draggable="true" @dragstart="startDrag($event)">
          <div class="piece-cell" :class="{ colored: cell }" @mousedown="on_mouse_down(index)" v-for="(cell, index) in grid.flat()" :key="index"></div>
        </div>
      </div>
      <button class="transparent-button" :class="{invisible: !(hovering && canRotate)}" @click="rotate(-1)">⤸</button>
    </div>
    <div class="flex-center-content">
      <button class="centered transparent-button" :class="{invisible: !(hovering && canFlip)}" @click="flip">⮍</button>
    </div>
  </div>
</template>