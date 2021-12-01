package main

import "fmt"

func main() {
	var R0, R1, R2, R3, R4, R5 int

	R0 = 9079325

	// follow is disassembly

	R4 = 0

	for {
		R5 = R4 | 65536
		R4 = 1855046

		for {
			R2 = R5 & 255
			R4 = R4 + R2
			R4 = R4 & 16777215
			R4 = R4 * 65899
			R4 = R4 & 16777215

			if R5 >= 256 {
				break
			}

			R2 = 0

			for {
				R1 = R2 + 1
				R1 = R1 * 256

				if R1 > R5 {
					break
				}

				R2 = R2 + 1
			}

			R5 = R2
		}

		fmt.Println("COUCOU:", R4, R0)
		if R4 == R0 {
			break
		}
	}

	// end of disassembly

	fmt.Println("R0:", R0, "R1:", R1, "R2:", R2, "R3:", R3, "R4:", R4, "R5:", R5)
}
