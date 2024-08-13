<script setup>
</script>
<style scoped>
  .mainbox {
    background-color: white;
    margin: auto;
    height: 600px;
    width: 600px;
    position: relative;
  }
  .err {
    color: green;
    font-family: sans-serif;
    font-size: 11rem;
    position:absolute;
    left: 30%;
    top: 0%;
  }
  .msg {
    text-align: center;
    font-family: sans-serif;
    font-size: 1.6rem;
    position:absolute;
    left: 16%;
    top: 45%;
    width: 75%;
  }
  a {
    text-decoration: none;
    color: blue;
  }
  a:hover {
    text-decoration: underline;
  }
</style>
<template>
  <div class="mainbox">
    <div class="err">404</div>    
    <div class="msg">
      Страница не найдена
      <p>
        Возможно, тут что-то было или появится в будущем, но сейчас здесь ничего нет.
      </p>
      <p>
        Попробуйте главную 
        <RouterLink to="/">страницу</RouterLink>.
      </p>
    </div>
  </div>
</template>