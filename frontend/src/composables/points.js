import { ref, toValue, watchEffect } from 'vue'

export function usePoints(points){
    const grid = ref([])
    const left = ref(0)
    const width = ref(0)
    const diameter = ref(0)

    const process = () => {
        const _points = toValue(points)
        const maxX = Math.max(..._points.map((point) => point[1]))
        const minX = Math.min(..._points.map((point) => point[1]))
        const maxY = Math.max(..._points.map((point) => point[0]))
        const _width = maxX - minX + 1
        const _height = maxY + 1
        left.value = minX
        width.value = _width
        diameter.value = Math.max(_width, _height)    
    
        const _grid = Array(maxY + 1).fill().map(()=>Array(_width).fill(false))
        for (const [y, x] of _points){
          _grid[y][x - minX] = true
        }
        grid.value = _grid
    }

    watchEffect(process)

    return {left, width, diameter, grid }
}
