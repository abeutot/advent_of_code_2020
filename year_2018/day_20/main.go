package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
)

const (
	UNKNOWN = uint8(0)
	DOOR    = uint8(1)
	ROOM    = uint8(2)
	WALL    = uint8(3)
)

type World struct {
	world                                  [300][300]uint8
	startX, startY, minX, maxX, minY, maxY int
}

func NewWorld() *World {
	w := new(World)

	w.startX = len(w.world) / 2
	w.startY = len(w.world[0]) / 2
	w.minX = len(w.world) - 1
	w.maxX = 0
	w.minY = len(w.world[0]) - 1
	w.maxY = 0

	return w
}

func (w *World) minMax(x, y int) {
	if x < w.minX {
		w.minX = x
	}
	if x > w.maxX {
		w.maxX = x
	}
	if y < w.minY {
		w.minY = y
	}
	if y > w.maxY {
		w.maxY = y
	}
}

func (w *World) wallify() {
	for j := w.minY - 1; j <= w.maxY+1; j++ {
		for i := w.minX - 1; i <= w.maxX+1; i++ {
			if w.world[i][j] == UNKNOWN {
				w.world[i][j] = WALL
			}
		}
	}
}

func (w *World) stringifyWorld() string {
	result := ""

	for j := w.minY - 1; j <= w.maxY+1; j++ {
		for i := w.minX - 1; i <= w.maxX+1; i++ {
			if i == w.startX && j == w.startY {
				result += "X"
				continue
			}

			switch w.world[i][j] {
			case UNKNOWN:
				result += "?"
			case DOOR:
				if w.world[i+1][j] == ROOM || w.world[i-1][j] == ROOM {
					result += "|"
				} else {
					result += "-"
				}
			case ROOM:
				result += "."
			case WALL:
				result += "#"
			}
		}
		result += "\n"
	}

	return result
}

func (w *World) followTheRegex(regex []byte, regexPos, wx, wy int, nextBranch []int) {
	fmt.Println("x:", wx, "y:", wy, "re:", string(regex[regexPos]), regexPos)

	w.minMax(wx, wy)

	w.world[wx-1][wy-1] = WALL
	w.world[wx+1][wy-1] = WALL
	w.world[wx-1][wy+1] = WALL
	w.world[wx+1][wy+1] = WALL
	w.world[wx][wy] = ROOM

	// fmt.Println("pos:", regexPos)
	switch regex[regexPos] {
	case 'N':
		w.world[wx][wy-1] = DOOR
		w.followTheRegex(regex, regexPos+1, wx, wy-2, nextBranch)
	case 'S':
		w.world[wx][wy+1] = DOOR
		w.followTheRegex(regex, regexPos+1, wx, wy+2, nextBranch)
	case 'E':
		w.world[wx+1][wy] = DOOR
		w.followTheRegex(regex, regexPos+1, wx+2, wy, nextBranch)
	case 'W':
		w.world[wx-1][wy] = DOOR
		w.followTheRegex(regex, regexPos+1, wx-2, wy, nextBranch)
	case '(':
		parenCount := 1
		pairParen := regexPos + 1
		for ; parenCount > 0; pairParen++ {
			if regex[pairParen] == ')' {
				parenCount--
			} else if regex[pairParen] == '(' {
				parenCount++
			}
		}

		fmt.Println("pair:", pairParen, string(regex[pairParen]))

		w.followTheRegex(regex, regexPos+1, wx, wy, append(nextBranch, pairParen))

		parenCount = 0
		for op := regexPos + 1; op < pairParen; op++ {
			if regex[op] == '(' {
				parenCount++
			} else if regex[op] == ')' {
				parenCount--
			}

			if parenCount == 0 && regex[op] == '|' {
				w.followTheRegex(regex, op+1, wx, wy, append(nextBranch, pairParen))
			}
		}
	case ')', '|':
		if len(nextBranch) > 0 {
			w.followTheRegex(regex, nextBranch[len(nextBranch)-1], wx, wy, nextBranch[:len(nextBranch)-1])
		}
	case '$':
		return
	}
}

func (w *World) FollowTheRegex(regex []byte) {
	if regex[0] != '^' || regex[len(regex)-1] != '$' {
		panic("invalid input")
	}

	w.followTheRegex(regex, 1, w.startX, w.startY, []int{})

	w.wallify()
}

func (w *World) shortestPaths(x, y int) {
	/* TODO */
}

func (w *World) ShortestPath() {

}

func main() {
	regex, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	regex = bytes.TrimRight(regex, "\n")

	w := NewWorld()

	w.FollowTheRegex(regex)

	fmt.Println(w.stringifyWorld())
}
