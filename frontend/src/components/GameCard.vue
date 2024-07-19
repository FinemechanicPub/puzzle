<script setup>
    import { computed} from 'vue'

    import { OpenAPI } from  '@/api/generated/core/OpenAPI'

    const props = defineProps({
        game: Object
    })
    const thumbnailUrl = computed(
        () => `${OpenAPI.BASE}/api/v1/games/${props.game.id}/thumbnail`
    )
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
        <p>
            {{ props.game.title }}
        </p>
        <img :src="thumbnailUrl" alt="game thumbnail">
    </div>

</template>