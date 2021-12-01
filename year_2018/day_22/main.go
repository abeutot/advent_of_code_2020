package main

import "fmt"

const DEBUG = false

const (
	ROCKY  = 0
	WET    = 1
	NARROW = 2
)

func abs(v int) int {
	if v < 0 {
		return -v
	}

	return v
}

type CacheKey struct {
	x, y int
}

var caching = func() map[CacheKey]int {
	return make(map[CacheKey]int)
}()

func erosionLevel(x, y int) int {
	return (geologicIndex(x, y) + depth) % 20183
}

func geologicIndex(x, y int) int {
	if x == 0 && y == 0 {
		return 0
	}

	if x == targetX && y == targetY {
		return 0
	}

	if y == 0 {
		return x * 16807
	}

	if x == 0 {
		return y * 48271
	}

	result, found := caching[CacheKey{x: x, y: y}]
	if found {
		return result
	}

	result = erosionLevel(x-1, y) * erosionLevel(x, y-1)
	caching[CacheKey{x: x, y: y}] = result

	return result
}

func type_(x, y int) int {
	return erosionLevel(x, y) % 3
}

func riskLevel() int {
	result := 0

	for j := 0; j <= targetY; j++ {
		for i := 0; i <= targetX; i++ {
			t := type_(i, j)
			switch t {
			case ROCKY:
				print(".")
			case WET:
				print("=")
			case NARROW:
				print("|")
			}
			result += t
		}
		println("")
	}

	return result
}

const (
	NEITHER  = 0
	TORCH    = 1
	CLIMBING = 2
)

const MAX = int(^uint(0) >> 1)

var TRANSITIONS = func() [4][3][4][3]int {
	var t [4][3][4][3]int

	/* allowed items
	   ROCKY -> CLIMBING,TORCH
	   WET -> CLIMBING,NEITHER
	   NARROW -> TORCH,NEITHER
	*/

	t[ROCKY][CLIMBING][ROCKY][CLIMBING] = 1
	t[ROCKY][CLIMBING][WET][CLIMBING] = 1
	t[ROCKY][CLIMBING][NARROW][TORCH] = 8
	t[ROCKY][TORCH][ROCKY][TORCH] = 1
	t[ROCKY][TORCH][WET][CLIMBING] = 8
	t[ROCKY][TORCH][NARROW][TORCH] = 1
	t[WET][CLIMBING][ROCKY][CLIMBING] = 1
	t[WET][CLIMBING][WET][CLIMBING] = 1
	t[WET][CLIMBING][NARROW][NEITHER] = 8
	t[WET][NEITHER][ROCKY][CLIMBING] = 8
	t[WET][NEITHER][WET][NEITHER] = 1
	t[WET][NEITHER][NARROW][NEITHER] = 1
	t[NARROW][TORCH][ROCKY][TORCH] = 1
	t[NARROW][TORCH][WET][NEITHER] = 8
	t[NARROW][TORCH][NARROW][TORCH] = 1
	t[NARROW][NEITHER][ROCKY][TORCH] = 8
	t[NARROW][NEITHER][WET][NEITHER] = 1
	t[NARROW][NEITHER][NARROW][NEITHER] = 1

	return t
}()

func minMinutes() int {
	type Path struct {
		x, y      int
		time      int
		equipment int
	}
	type CacheEqKey struct {
		x, y, eq int
	}
	unvisited := make(map[CacheEqKey]*Path)
	visited := make(map[CacheEqKey]*Path)

	unvisited[CacheEqKey{x: 0, y: 0, eq: TORCH}] = &Path{x: 0, y: 0, time: 0, equipment: TORCH}

	for {
		/* select the minimum of the unvisited as current */
		var current *Path = nil

		for _, candidate := range unvisited {
			if current == nil || current.time > candidate.time {
				current = candidate
			}
		}

		if current == nil {
			break
		}

		currentType := type_(current.x, current.y)

		/* let's explore the neighbors */
		for i := -1; i < 2; i++ {
			for j := -1; j < 2; j++ {
				if abs(i) == abs(j) {
					/* ignore self and diagonals */
					continue
				}

				if current.x+i < 0 || current.y+j < 0 || current.x+i > targetX+100 || current.y+j > targetY+100 {
					/* out of bounds */
					continue
				}

				nType := type_(current.x+i, current.y+j)

				for nextEquipment := NEITHER; nextEquipment <= CLIMBING; nextEquipment++ {
					cost := TRANSITIONS[currentType][current.equipment][nType][nextEquipment]
					if cost == 0 {
						continue
					}

					if _, found := visited[CacheEqKey{x: current.x + i, y: current.y + j, eq: nextEquipment}]; found {
						continue
					}

					p := &Path{x: current.x + i, y: current.y + j, time: current.time + cost, equipment: nextEquipment}
					ck := CacheEqKey{x: p.x, y: p.y, eq: nextEquipment}
					u, found := unvisited[ck]
					if !found || u.time > p.time {
						unvisited[ck] = p
					}
				}
			}
		}

		/* mark as visited */
		ck := CacheEqKey{x: current.x, y: current.y, eq: current.equipment}
		visited[ck] = current
		delete(unvisited, ck)
	}

	a, found := visited[CacheEqKey{x: targetX, y: targetY, eq: TORCH}]
	if found {
		b, found := visited[CacheEqKey{x: targetX, y: targetY, eq: CLIMBING}]
		if found {
			if b.time+7 < a.time {
				return b.time + 7
			}
		}

		return a.time
	}

	return -1
}

var targetX, targetY = 10, 10
var depth = 510

func main() {
	if !DEBUG {
		targetX, targetY, depth = 15, 740, 3558
	}

	fmt.Println("riskLevel:", riskLevel())

	fmt.Println("min minutes:", minMinutes())
}
