async function getHint(gameId, installedPieces){
    var uri = `${import.meta.env.VITE_API_BASE_URI}/play/hint/`
    const requestOptions = {
        method: "PUT",
        headers: { "Content-Type": "application/json; charset=utf-8" },
        body: JSON.stringify(
            {
                game_id: gameId,
                pieces: installedPieces
            }
        ) 
    }
    console.log(requestOptions.body)
    var response = await fetch(uri, requestOptions)
    var hint = await response.json()
    return hint
}

export default getHint;