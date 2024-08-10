<script setup>
  import { computed, ref } from 'vue'

  import divmod from '@/utils/divmod'

  const props = defineProps({
    piece: Object,
    cellSize: Number
  })
  const emit = defineEmits(['pieceTouch'])

  const cell_width = `${props.cellSize - 2}px`

  const hovering = ref(false)

  const rotationIndex = ref(0)
  const rotation = computed(() => props.piece.rotations[rotationIndex.value]) 
  const points = computed(() => rotation.value.points)
  const colorString =  computed(() => `#${props.piece.color.toString(16)}`)
  const maxX = computed(() => Math.max(...points.value.map((point) => point[1])))
  const minX = computed(() => Math.min(...points.value.map((point) => point[1])))
  const maxY = computed(() => Math.max(...points.value.map((point) => point[0])))
  const diameter = computed(() => (1 + Math.max(maxX.value - minX.value, maxY.value)))
  const box_width = computed(() => `${diameter.value*(props.cellSize)}px`)
  const grid = computed(make_grid)
  const width = computed(() => maxX.value - minX.value + 1)
  const canFlip = computed(() => props.piece.rotations.length > 4)
  const canRotate = computed(() => props.piece.rotations.length > 1)
  
  const mouse_index = ref(null)

  const touchStart = ref([])
  const touchCurrent = ref([])
  const scrollShift = ref(0)
  const touchShiftX = computed(() => Math.round(touchCurrent.value.length ? touchCurrent.value[0] - touchStart.value[0] : 0) + "px")
  const touchShiftY = computed(() => Math.round(touchCurrent.value.length ? touchCurrent.value[1] - touchStart.value[1] - scrollShift.value : 0) + "px")


  function make_grid(){
    const grid = Array(maxY.value + 1).fill().map(()=>Array(maxX.value - minX.value + 1).fill(false))
    for (const [y, x] of points.value){
      grid[y][x - minX.value] = true
    }
    return grid
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


  function onTouchStart(evt, index){
    touchCurrent.value = []
    touchStart.value = [evt.touches[0].clientX, evt.touches[0].clientY]
    scrollShift.value = 0
    mouse_index.value = index
    console.log("touch start", touchStart.value[0], touchStart.value[1])
  }

  function onTouchMove(evt){
    const [x, y] = [evt.touches[0].clientX, evt.touches[0].clientY]
    const currentScroll = Math.round(window.scrollY)
    if (y < 150 && currentScroll){
      console.log("scroll")
      window.scrollTo({top: 0, behavior: "instant"})
      scrollShift.value += currentScroll
    }
    touchCurrent.value = [x, y]
  }

  function onTouchEnd(){
    const [dy, dx] = divmod(mouse_index.value, width.value)
    const piece_data = {
      dy: -dy,
      dx: -dx - minX.value,
      pieceId: props.piece.id,
      rotationId: rotation.value.id,
      touchXY: touchCurrent.value
    }
    touchCurrent.value = []
    console.log("touch end")
    emit("pieceTouch", piece_data)
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
    width: v-bind(cell_width);
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
    width: v-bind(box_width);
    height: v-bind(box_width);
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

  .movable{
    transform: translate(v-bind(touchShiftX), v-bind(touchShiftY));
    touch-action: none;
  }
</style>

<template>
  <div class="hover" @mouseenter="hovering=true" @mouseleave="hovering=false">
    <div class="container-row" >
      <button class="transparent-button" :class="{invisible: !(hovering && canRotate)}" @click="rotate(1)">↪️</button>
      <div class="piece-box movable">
        <div class="piece grid cursor-pointer" draggable="true" @dragstart="startDrag($event)">
          <div class="piece-cell" :class="{ colored: cell }" @mousedown="on_mouse_down(index)" v-for="(cell, index) in grid.flat()" :key="index" @touchstart="onTouchStart($event, index)" @touchmove="onTouchMove($event)" @touchend="onTouchEnd()"></div>
        </div>
      </div>
      <button class="transparent-button" :class="{invisible: !(hovering && canRotate)}" @click="rotate(-1)">↩️</button>
    </div>
    <div class="flex-center-content">
      <button class="centered transparent-button" :class="{invisible: !(hovering && canFlip)}" @click="flip">🔄</button>
    </div>
  </div>
</template>