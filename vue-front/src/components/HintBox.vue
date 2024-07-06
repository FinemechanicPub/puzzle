<script setup>
    import { computed, ref, watchEffect } from 'vue';

    import getHint from '@/api/hint';

    const props = defineProps({
        gameId: Number,
        installedPices: Array
    })

    const emit = defineEmits(['hint'])
    
    const loading = ref(false)
    const error = ref(null)
    const hint = ref(null)
    const hintActive = ref(true)

    const message = computed(
        () => loading.value ? " ...запрашиваю Центр... " : (
            hint.value ? "могу подсказать ход" : error.value
        )
    )

    watchEffect(fetchHint)

    async function fetchHint(){
        hint.value = null
        error.value = null
        if (!hintActive.value || props.installedPices.length == 0) return;

        loading.value = true
        try{
            const data = await getHint(props.gameId, props.installedPices.map((item)=> ({piece_id: item.piece.id, rotation_id: item.rotation.id, position: item.index})))
            // progress = 1
            // complete = 2
            // deadlock = 3
            if (data.status == 3) {
                error.value = "безвыходная ситуация"
            } else if (data.status == 2) {
                error.value = ""
            } else {
                hint.value = Object.values(data.hint)
            }
        } catch (err) {
            if (err instanceof TypeError){
                error.value = "Нет связи с Центром"
            } else {
                error.value = err.toString()
            }
        } finally{
            loading.value = false
        }
    }
</script>

<template>
    <div class="hint-box">
        <p @click="hintActive = !hintActive" class="hint-item transparent-button">🤖</p>
        <p class="hint-item">
            {{ message }}
        </p>
        <button @click="emit('hint', hint)" class="hint-item transparent-button" v-if="hint">🆗</button>
        <button @click="fetchHint" class="hint-item transparent-button" v-if="error">↩️</button>
    </div>
</template>