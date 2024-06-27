async function getGame(gameId){
    // fetch("/games/17/full/").then((response) => {
    //     response.json().then((data) => {
            
    //     })
    // })
    var uri = `${import.meta.env.VITE_API_BASE_URI}/games/${gameId}/full/`
    console.log(import.meta.env)
    console.log(uri)
    var response = await fetch(uri)
    console.log(response)
    var game = await response.json()
    return game
}

export default getGame;
