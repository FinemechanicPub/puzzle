<script setup>

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
  const steps = [
    {
      target: '#board',  // We're using document.querySelector() under the hood
      header: {
          title: 'Доска',
      },
      content: "Все ячейки доски нужно закрыть фигурами без наложения одной на другую.",
      params: {
          highlight: true
      }
    },
    {
        target: '#palette',
        header: {
            title: 'Магазин фигур'
        },
        content: "Здесь лежат все доступные фигуры. Фигура устанавливается на доску перетаскиванием."
    },
    {
        target: 'div.square:nth-child(1)',
        content: "Чтобы удалить фигуру с доски обратно в магазин, щелкните по любой её клетке."
    },
    {
        target: 'div.palette-item',
        content: "Если навести курсор на фигуру, появятся кнопки вращения и переворота, если это можно сделать."
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
        content: "Если нажать на эту кнопку, робот поставит подходящую по его мнению фигуру на доску."
    },
    {
        target: '#robotswitch',
        content: "С помощью этой кнопки подсказки робота можно отключить."
    }
  ]

</script>

<template>
  <v-tour name="gameTour" :steps="steps" :options="options"></v-tour>
</template>
