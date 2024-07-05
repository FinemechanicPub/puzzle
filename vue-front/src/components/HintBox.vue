<script setup>
    import { computed, ref, watch } from 'vue';

    import getHint from '@/api/hint';

    const props = defineProps({
        gameId: Number,
        installedPices: Array
    })

    const emit = defineEmits(['hint'])
    
    const loading = ref(false)
    const error = ref(null)
    const hint = ref(null)
    
    const message = computed(
        () => loading.value ? " ...запрашиваю Центр... " : (
            hint.value ? "могу подсказать ход" : error.value
        )
    )


    watch(props.installedPices, fetchHint)

    async function fetchHint(){
        hint.value = null
        error.value = null
        loading.value = true
        try{
            const data = await getHint(props.gameId, props.installedPices.map((item)=> ({piece_id: item.piece.id, rotation_id: item.rotation.id, position: item.index})))
            if (!data){
                error.value = "безвыходная ситуация"
            } else {
                hint.value = Object.values(data)
            }
        } catch (err) {
            error.value = err.toString()
        } finally{
            loading.value = false
        }
    }
</script>

<template>
    <div class="hint-box">
        <p class="hint-item">🤖</p>
        <p class="hint-item">
            {{ message }}
        </p>
        <button @click="emit('hint', hint)" class="hint-item" v-if="hint">Давай</button>
    </div>
</template>