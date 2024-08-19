<script setup>
</script>
<style scoped>
  .mainbox {
    background-color: var(--color-background);
    text-align: center;
    margin: auto 5%;
  }
  .err {
    color: var(--color-text);
    font-family: sans-serif;
    font-size: 11rem;
  }
  .msg {
    text-align: center;
    font-family: sans-serif;
    font-size: 1.6rem;
  }
</style>
<template>
  <div class="mainbox">
    <div class="err">404</div>    
    <div class="msg">
      Страница не найдена.
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