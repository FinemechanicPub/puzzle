<script setup>
    import PieceItem from '@/components/PieceItem.vue';

    const props = defineProps({
        availablePieces: Array,
        cellSize: Number
    })

    const emit = defineEmits(["pieceTouch"])

    function onPieceTouch(data){
        emit("pieceTouch", data)
    }
</script>

<style scoped>
    .palette-item{
        align-content: center;
    }
</style>

<template>
	<div class="piece-palette" v-auto-animate>
        <div class="palette-item" :key="piece.id" v-for="piece in props.availablePieces">
            <PieceItem @piece-touch="onPieceTouch" :piece="piece" :cell-size="cellSize"/>
        </div>
    </div>
</template>
