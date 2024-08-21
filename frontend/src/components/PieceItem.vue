<script setup>
  import { computed, ref } from 'vue'

  import divmod from '@/utils/divmod'
  import { usePoints } from '@/composables/points'
  import { useTransform } from '@/composables/transform'

  const props = defineProps({
    piece: Object,
  })
  const emit = defineEmits(['pieceTouch', 'changeVersion'])

  const cells = ref([])

  const hovering = ref(false)

  const rotation = computed(() => props.piece.rotations[props.piece.base_version]) 
  const points = computed(() => rotation.value.points)
  const colorString =  computed(() => `#${props.piece.color.toString(16)}`)
  const { left, width, diameter, grid } = usePoints(points)
  const { flip, rotate } = useTransform(props.piece.rotations)

  const mouse_index = ref(null)

  const touchStart = ref([])
  const touchCurrent = ref([])
  const scrollShift = ref(0)
  const touchShiftX = computed(() => Math.round(touchCurrent.value.length ? touchCurrent.value[0] - touchStart.value[0] : 0) + "px")
  const touchShiftY = computed(() => Math.round(touchCurrent.value.length ? touchCurrent.value[1] - touchStart.value[1] - scrollShift.value : 0) + "px")

  function on_mouse_down(index){
    console.log(`mouse down in cell #${index}`)
    mouse_index.value = index
  }

  function startDrag(evt){
      console.log('dragging piece')
      const [dy, dx] = divmod(mouse_index.value, width.value)
      const pieceRect = evt.target.getBoundingClientRect()
      const cellSize = Math.max(pieceRect.height, pieceRect.width) / diameter.value      
      const halfSize = cellSize / 2
      const offsetX = Math.round(evt.clientX - pieceRect.left) % cellSize - halfSize
      const offsetY = Math.round(evt.clientY - pieceRect.top) % cellSize - halfSize
      const piece_data = {
        dy: -dy,
        dx: -dx - left.value,
        pieceId: props.piece.id,
        rotationId: rotation.value.id,
        offsetX: offsetX,
        offsetY: offsetY
      }
      evt.dataTransfer.dropEffect = 'move'
      evt.dataTransfer.effectAllowed = 'move'
      evt.dataTransfer.setData('piece_data', JSON.stringify(piece_data))
  }


  function onTouchStart(evt, index){
    touchCurrent.value = []
    const [clientX, clientY] = [evt.touches[0].clientX, evt.touches[0].clientY]
    // Find touched cell
    // "It should be noted that the ref array does not guarantee the same order as the source array."
    // https://vuejs.org/guide/essentials/template-refs.html#refs-inside-v-for
    for (const cell of cells.value){
      const cellRect = cell.getBoundingClientRect()
      if (
        clientX > cellRect.left && clientX < cellRect.right
        && clientY > cellRect.top && clientY < cellRect.bottom
      ) {
        touchStart.value = [(cellRect.left + cellRect.right) / 2, (cellRect.top + cellRect.bottom) / 2]
        break
      }

    }
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
      dx: -dx - left.value,
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
    width: calc(var(--cell-width) - 2px);
    margin: 1px;
  }
  .colored {
    background-color: v-bind(colorString);
  }
  .container-row{
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .piece-box{
    display: flex;
    align-items: center;
    justify-content: center;
    width: calc(var(--cell-width) * v-bind(diameter));
    height: calc(var(--cell-width) * v-bind(diameter));
    margin: 0.3rem;
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
  .padded{
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
</style>

<template>
  <div class="hover" @mouseenter="hovering=true" @mouseleave="hovering=false">
    <div class="container-row" >
      <button type="button" title="повернуть влево" class="transparent-button" :class="{invisible: !(hovering && rotate)}" @click="emit('changeVersion', rotate(props.piece.base_version, 1))">
        ↪️
      </button>
      <div class="piece-box movable">
        <div class="piece grid cursor-pointer" draggable="true" @dragstart="startDrag($event)">
          <div class="piece-cell" :class="{ colored: cell }" ref="cells"
            v-for="(cell, index) in grid.flat()"
            :key="index"
            @mousedown="on_mouse_down(index)"
            @touchstart="onTouchStart($event, index)"
            @touchmove="onTouchMove($event)"
            @touchend="onTouchEnd()"
            >
          </div>
        </div>
      </div>
      <button type="button" title="повернуть вправо" class="transparent-button" :class="{invisible: !(hovering && rotate)}" @click="emit('changeVersion', rotate(props.piece.base_version, -1))">
        ↩️
      </button>
    </div>
    <div class="flex-center-content">
      <button type="button" title="перевернуть сверху вниз" class="centered padded transparent-button" :class="{invisible: !(hovering && flip)}" @click="emit('changeVersion', flip(props.piece.base_version, false))">
        🔃
      </button>
      <button type="button" title="перевернуть слева направо" class="centered padded transparent-button" :class="{invisible: !(hovering && flip)}" @click="emit('changeVersion', flip(props.piece.base_version, true))">
        🔄
      </button>
    </div>
  </div>
</template>