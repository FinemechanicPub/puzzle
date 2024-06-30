async function getGame(gameId){
    var uri = `${import.meta.env.VITE_API_BASE_URI}/games/${gameId}/full/`
    var response = await fetch(uri)
    var game = await response.json()
    return game
}

export default getGame;
