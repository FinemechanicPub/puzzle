<script setup>
    import { ref } from 'vue';
    import { OpenAPI } from  '@/api/generated/core/OpenAPI';
    import { useRouter } from 'vue-router'

    const props = defineProps({
        games: Array
    })
    const router = useRouter()
    const currentIndex = ref(0)
    const thumbnailUrl = (game) => `${OpenAPI.BASE}/api/v1/games/${game.id}/thumbnail/`

    let startX, moveX;

    function touchStart(evt) {
      startX = evt.touches[0].pageX;
    }

    function touchMove(evt) {
      moveX = evt.touches[0].pageX;
    }

    function touchEnd() {
      if (startX - moveX > 50 && currentIndex.value < props.games.length - 1) {
            nextCard();
          } else if (moveX - startX > 50 && currentIndex.value > 0) {
            prevCard();
          }
    }

    function nextCard(){
        currentIndex.value++;
    }
    function prevCard(){
        currentIndex.value--;
    }

    function gameWon(game_id){
      const savedGame = localStorage.getItem(`puzzleWin${game_id}`)
      if (savedGame) {
        return true
      }
      return false
    }
</script>

<style scoped>
  .carousel-container {
    width: 80%;
    max-width: 1000px;
    margin: 2rem auto;
    overflow: hidden;
    position: relative;
  }
  .carousel {
    display: flex;
    transition: transform 0.5s ease;
    padding: 20px 0; /* Added padding to prevent shadow cutoff */
  }
  .card {
    flex: 0 0 270px;
    height: 400px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 0 10px 0px rgba(0,0,0,0.2);
    margin: 0 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px;
    box-sizing: border-box;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  .card h2 {
    color: #333;
    margin-top: 0;
  }
  .card p {
    color: #666;
    line-height: 1.6;
  }
  .card .cta-button {
    background-color: #333;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  .card .cta-button:hover {
    color: #ffd700;
  }
  .card img {
    width: 100%;
    height: 280px;
    object-fit: contain;
    border-radius: 5px;
    margin-bottom: 10px;    
  }
  .carousel-button {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background-color: rgba(0,0,0,0.5);
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    font-size: 18px;
    transition: background-color 0.3s ease;
  }
  .carousel-button:hover {
    background-color: rgba(0,0,0,0.8);
    color: #ffd700;
  }
  .carousel-button.prev {
    left: 12px;
  }
  .carousel-button.next {
    right: 0px;
  }
  .medal {
    position: absolute;
    top: 10%;
    font-size: larger;
  }
</style>
<template>
    <div class="carousel-container">
        <div class="carousel"
          @touchstart="touchStart($event)"
          @touchmove="touchMove($event)"
          @touchend="touchEnd"
          :style="{ transform: `translateX(${-currentIndex * 290}px)` }"
          > 
            <div v-if="games.length===0" class="card">
              <h2>Не удалось найти ничего подходящего</h2>
            </div>         
            <div v-for="game in games" :key="game.id" class="card">
                <h2>{{ game.title }}</h2><p class="medal" v-if="gameWon(game.id)">🏅</p>
                <p></p>
                <div>
                    <img :src="thumbnailUrl(game)" alt="game thumbnail">
                </div>
                <button type="button" @click="router.push({name: 'game', params: {id: game.id}})" class="cta-button">
                  Играть
                </button>
            </div>
        </div>
        <button type="button" v-if="games.length > 1" class="carousel-button prev" @click="prevCard" :disabled="currentIndex === 0">&lt;</button>
        <button type="button" v-if="games.length > 1" class="carousel-button next" @click="nextCard" :disabled="currentIndex === games.length - 1">&gt;</button>
    </div>
</template>