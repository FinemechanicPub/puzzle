import { ref, toValue } from 'vue';

export function useTransform(rotations){
    const rotate = ref(null)
    const flip = ref(null)

    const _rotations = toValue(rotations)
    const length = _rotations.length
    const canRotate = length > 1
    const flipIndex = 1 + _rotations.findLastIndex((item) => item.flipped === 0)
    const canFlip = flipIndex < length

    function _rotate(index, turns) {
        if (canFlip){
            const half_length = length / 2
            if (index < half_length){
                return (half_length + index + turns) % half_length
            } else {
                return half_length + (index - turns) % half_length
            }
        } else { // no flips for this piece
            return (length + index + turns) % length
        }
    }

    function _flip(index, horizontal){
        const cycleLength = length > 2 ? Math.floor(length / 2) : 0
        const new_index = (index + cycleLength) % length
        if (horizontal && flipIndex > 2){
            return _rotate(new_index, 2)
        }
        return new_index
    }

    rotate.value = canRotate ? _rotate : null
    flip.value = canFlip ? _flip : null

    return { flip, rotate }
}
