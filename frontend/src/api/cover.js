async function getGames(){
    var uri = `${import.meta.env.VITE_API_BASE_URI}/cover/suggestion/`
    var response = await fetch(uri, { headers: { "Content-Type": "application/json; charset=utf-8" }})
    var game = await response.json()
    return game
}

export default getGames;