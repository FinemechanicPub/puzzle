<script setup>
    import { computed, ref, watchEffect } from 'vue';

    import { ApiError, gamesHint } from '@/api/generated/'

    const props = defineProps({
        gameId: Number,
        installedPices: Array
    })

    const emit = defineEmits(['hint'])
    
    const loading = ref(false)
    const error = ref(null)
    const hint = ref(null)
    const info = ref(null)
    const hintActive = ref(true)

    const message = computed(
        () => loading.value ? " ...запрашиваю Центр... " : (
            hint.value ? "могу подсказать ход" : (
                info.value ? info.value : error.value
            )
        )
    )

    watchEffect(fetchHint)

    async function fetchHint(){
        hint.value = null
        info.value = null
        error.value = null
        if (!hintActive.value) return;

        loading.value = true

        try {
            const data = await gamesHint({
                requestBody: {
                    game_id: props.gameId,
                    pieces: props.installedPices.map(
                        (item)=> ({
                            piece_id: item.piece.id,
                            rotation_id: item.rotation.id,
                            position: item.index
                        })
                    )
                }
            })
            // progress = 1
            // complete = 2
            // deadlock = 3
            if (data.status == 3) {
                info.value = "безвыходная ситуация"
            } else if (data.status == 2) {
                error.value = ""
            } else {
                hint.value = Object.values(data.hint)
            }
        } catch (err) {
            console.log("fetching a hint caused the error: ", err.toString())
            if (err instanceof ApiError){
                error.value = "Нет связи с Центром"
            } else {
                error.value = err.toString()
            }
        } finally {
            loading.value = false
        }
    }
</script>

<style scoped>
.hint-box{
    padding: 1rem;
}
</style>

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