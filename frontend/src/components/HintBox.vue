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
    const complete = ref(false)
    const hintActive = ref(true)
    const hasHint = computed(() => hint.value !== null)
    
    const message = computed(
        () => loading.value ? " ...запрашиваю Центр... " : (
            error.value ? error.value : (
                hasHint.value ? "могу подсказать ход" : "безвыходная ситуация"
            )
        )
    )

    watchEffect(fetchHint)

    async function fetchHint(){
        hint.value = null
        complete.value = false
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
            if (data.status == 1) {
                hint.value = Object.values(data.hint)
            } else if (data.status == 2) {
                complete.value = true
            }
            error.value = ""
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

    defineExpose({
        hasHint: hasHint
    })
</script>

<style scoped>
    .hint-box{
        display: inline-flex;
        align-items: center;
        height: 2rem;
        margin: 0.5rem auto;
        gap: 0.5rem;
    }
</style>

<template>
    <div class="hint-box">
        <button id="robotswitch" type="button" :title="complete ? 'отключено' : hintActive ? 'выключить' : 'включить'" @click="hintActive = !hintActive" :disabled="complete" class="hint-item transparent-button">
            🤖
        </button>
        <p v-if="hintActive && !complete" class="hint-item">
            {{ message }}
        </p>
        <button id="robotmove" type="button" title="пусть ходит робот" @click="emit('hint', hint)" class="hint-item transparent-button" v-if="hasHint">🆗</button>
        <p id="robotmove" v-else> </p>
        <button type="button" title="повторить запрос" @click="fetchHint" class="hint-item transparent-button" v-if="error">↩️</button>
    </div>
</template>