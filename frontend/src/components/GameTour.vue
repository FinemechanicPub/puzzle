<script setup>
  import { computed } from 'vue';
  const props = defineProps({
    hasHint: Boolean,
    hasPieces: Boolean
  })

  const options = {
      useKeyboardNavigation: true,
      highlight: true,
      labels: {
        buttonSkip: 'Пропустить',
        buttonPrevious: 'Назад',
        buttonNext: 'Вперед',
        buttonStop: 'Закончить'
      }
    }

  const steps = computed(() => [
    {
      target: '#board',
      header: {
          title: 'Доска',
      },
      content: "Все ячейки доски нужно закрыть фигурами без наложения одной на другую.",
    },
    {
      target: '#palette',
      header: {
          title: 'Магазин фигур'
      },
      content: "Здесь лежат все доступные фигуры. Фигура устанавливается на доску перетаскиванием.",
      params:{
        highlight: props.hasPieces
      }
    },
    {
      target: 'div.palette-item, #palette',
      content: "Если навести курсор на фигуру, появятся кнопки вращения и переворота. Вращение и переворот доступны не для всех фигур.",
      params:{
        highlight: props.hasPieces
      }
    },
    {
      target: 'div.square:nth-child(1)',
      content: "Чтобы удалить фигуру с доски обратно в магазин, щелкните по любой её клетке.",
      params: {
        highlight: false
      }
    },
    {
      target: '#hintbox',
      header: {
          title: 'Робот'
      },
      content: "Робот умеет решать головоломки, он может подсказать хороший ход."
    },
    {
      target: '#robotmove',
      content: props.hasHint ? "Если нажать на эту кнопку, робот поставит подходящую фигуру на доску." : "Сейчас у робота нет подсказок, поэтому кнопка хода роботом 🆗 скрыта.",
      params: {
        highlight: props.hasHint
      }
    },
    {
      target: '#robotswitch',
      content: "С помощью этой кнопки подсказки робота можно включать и отключать."
    },
    {
      target: '#info',
      content: "Чтобы посмотреть инструкции ещё раз, нажмите кнопку ℹ️ снова."
    }
  ]
)

</script>

<template>
  <v-tour name="gameTour" :steps="steps" :options="options"></v-tour>
</template>
