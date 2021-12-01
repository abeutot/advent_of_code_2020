package main

import "fmt"

const DEBUG = false

type CacheKey struct{ n, s int }

var cache = func() map[CacheKey]int {
	return make(map[CacheKey]int)
}()

func subjectNumber(number, loopSize int) int {
	iterStart := 0
	r, found := cache[CacheKey{n: number, s: loopSize - 1}]
	if found {
		iterStart = loopSize - 1
	} else {
		r = 1
	}

	for i := iterStart; i < loopSize; i++ {
		r = r * number % 20201227
	}

	cache[CacheKey{n: number, s: loopSize}] = r

	return r
}

func findLoopSize(number, expected int) int {
	for i := 0; ; i++ {
		if subjectNumber(number, i) == expected {
			return i
		}
	}

	return -1
}

func main() {
	doorPublic := 11404017
	cardPublic := 13768789

	if DEBUG {
		doorPublic = 17807724
		cardPublic = 5764801
	}

	doorSecret := findLoopSize(7, doorPublic)
	cardSecret := findLoopSize(7, cardPublic)

	fmt.Println("doop loop:", doorSecret, "card loop:", cardSecret)

	fmt.Println("part1:", subjectNumber(doorPublic, cardSecret), subjectNumber(cardPublic, doorSecret))
}
