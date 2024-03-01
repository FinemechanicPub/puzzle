<script>
export default {
  data() {
    return {
      msg: 'Hello World!',
      cells: ['F', 'F', 'F', ' ', ' ', ' ', 'X', ' ', ' '],
      width: 3,
      colors: {
        'F': 'cyan',
        'X': 'green',
        ' ': 'white'
      }
    }
  }
}
</script>
<style scoped>
.board {
  display: grid;
  grid-template-columns: repeat(v-bind(width), 1fr);
  border: 1px solid #999;
  width: fit-content;
}
.board > div {
  border: 1px solid #999;
  width: 20px;
  margin: 0px;
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1 / 1;
  
}
</style>

<template>
  <div class="board" >
    <div v-bind:style="{'background-color': colors[cell]}" v-for="cell, index in cells"></div>
  </div>
</template>