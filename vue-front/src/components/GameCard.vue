<script setup>
    const props = defineProps({
        game: Object
    })
</script>

<style scoped>
.rounded-box{
    border-radius: 10px;
    padding: 20px;
    margin: 1ch auto;
    width: -moz-fit-content;
    width: fit-content;
    font-weight: bolder;
    color: slateblue;
    background: mediumaquamarine;
    border: 2px solid lightseagreen;
    text-align: center; 
}

</style>

<template>
    <div class="rounded-box">
        {{ props.game.title }}
    </div>
</template>