<script setup>
    const props = defineProps({
        game: Object
    })
</script>

<style scoped>
.rounded-box{
    /* border-radius: 10px; */
    padding: 20px;
    margin: 1ch auto;
    width: -moz-fit-content;
    width: fit-content;
    font-weight: bolder;
    /* color: slateblue;
    background: mediumaquamarine; */
    /* border: 2px solid lightseagreen; */
    box-shadow: 0 0 .2rem #0000001a,0 .2rem .4rem #0003;
    text-align: center; 
}

</style>

<template>
    <div class="rounded-box">
        {{ props.game.title }}
    </div>
</template>