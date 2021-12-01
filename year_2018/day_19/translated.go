package main

import "fmt"

func main() {
	//R0, R1, R2, R3, R4 := 0, 0, 0, 0, 0
	R0, R2, R3 := 0, 0, 0

	R0 = 1 // part2

	R3 = 973
	if R0 != 0 {
		R3 = 10551373
		R0 = 0
	}

	for R2 = 1; R2 <= R3; R2++ {
		if R2%100 == 0 {
			fmt.Println("iteration:", R2)
		}

		/*
			for R1 = 1; R1 <= R3; R1++ {
				R4 = R1 * R2

				if R4 == R3 {
					R0 = R0 + R2
				}
			}
		*/

		/* optimized version of the upper loop */
		if R3%R2 == 0 {
			R0 += R2
		}
	}

	fmt.Println("R0:", R0)
}
