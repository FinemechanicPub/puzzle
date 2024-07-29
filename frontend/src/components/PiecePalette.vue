<script setup>
    import Piece from '@/components/Piece.vue';

    const props = defineProps({
        availablePieces: Array
    })
</script>

<template>
	<div class="piece-palette" v-auto-animate>
        <div class="palette-item" :key="piece.id" v-for="piece in props.availablePieces">
            <Piece :piece="piece"/>
        </div>
    </div>
</template>
