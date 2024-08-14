<script setup>
    import PieceItem from '@/components/PieceItem.vue';

    const props = defineProps({
        availablePieces: Array,
        cellSize: Number
    })

    const emit = defineEmits(["pieceTouch", "rotate", "flip"])

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
        <div class="palette-item" :key="piece.id" v-for="(piece, index) in props.availablePieces">
            <PieceItem
                @rotate="(to_index) => emit('rotate', to_index, index)"
                @flip="(to_index) => emit('flip', to_index, index)"
                @piece-touch="onPieceTouch"
                :piece="piece"
                :cell-size="cellSize"
            />
        </div>
    </div>
</template>
