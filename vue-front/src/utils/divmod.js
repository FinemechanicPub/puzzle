function divmod(divisor, divident){
    const quotinet = Math.floor(divisor / divident)
    const remainder = divisor % divident
    return [quotinet, remainder]
}

export default divmod;