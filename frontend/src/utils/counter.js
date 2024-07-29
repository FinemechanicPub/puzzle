function counter(list, attr="id"){

    let result = {}
    for (const item of list){
        const id = item[attr]
        if (!(id in result)){
            result[id] = 0
        }
        result[id]++
    }
    return result
}

export default counter;