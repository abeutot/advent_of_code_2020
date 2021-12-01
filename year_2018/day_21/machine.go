package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/signal"
	"strconv"
	"strings"
)

const DEBUG = false

var registers [6]int
var program [][4]int
var instrCounter []uint
var ip = 0

const (
	OP_BORI = 2
	OP_MULI = 13
	OP_MULR = 11
	OP_BORR = 9
	OP_ADDR = 10
	OP_ADDI = 15
	OP_SETI = 6
	OP_GTIR = 0
	OP_BANI = 12
	OP_BANR = 14
	OP_SETR = 1
	OP_EQRR = 8
	OP_EQIR = 5
	OP_GTRI = 4
	OP_GTRR = 3
	OP_EQRI = 7
)

var opcodesTranslator = map[string]int{
	"bori": OP_BORI,
	"muli": OP_MULI,
	"mulr": OP_MULR,
	"borr": OP_BORR,
	"addr": OP_ADDR,
	"addi": OP_ADDI,
	"seti": OP_SETI,
	"gtir": OP_GTIR,
	"bani": OP_BANI,
	"banr": OP_BANR,
	"setr": OP_SETR,
	"eqrr": OP_EQRR,
	"eqir": OP_EQIR,
	"gtri": OP_GTRI,
	"gtrr": OP_GTRR,
	"eqri": OP_EQRI,
}
var instrTranslator = func() map[int]string {
	t := make(map[int]string)

	for k := range opcodesTranslator {
		t[opcodesTranslator[k]] = k
	}

	return t
}()

func printInstr(i [4]int) {
	fmt.Print(instrTranslator[i[0]], " ", i[1], i[2], i[3])
}

func printProgram() {
	for i := range program {
		fmt.Print(i, ":\t")
		printInstr(program[i])
		fmt.Println("\t\t", instrCounter[i])
	}
}

func load_program(filepath string) {
	raw_content, err := ioutil.ReadFile(filepath)
	if err != nil {
		panic(err)
	}

	content := string(raw_content)

	instructions := strings.Split(strings.TrimRight(content, "\n"), "\n")

	for i := range instructions {
		s := strings.Split(instructions[i], " ")
		if i == 0 {
			if s[0] != "#ip" {
				continue
			}

			ip, _ = strconv.Atoi(s[1])
			continue
		}

		if len(s) != 4 {
			panic("invalid instruction length")
		}

		arg1, _ := strconv.Atoi(s[1])
		arg2, _ := strconv.Atoi(s[2])
		arg3, _ := strconv.Atoi(s[3])
		program = append(program, [4]int{
			opcodesTranslator[s[0]],
			arg1,
			arg2,
			arg3,
		})
	}

	instrCounter = make([]uint, len(program))
}

func execute_program(breakPoint int) {
	for {
		from := [2]byte{'i', 'i'}

		if registers[ip] >= len(program) {
			break
		}

		beforeIp := registers[ip]

		next_instruction := program[beforeIp]

		instrCounter[beforeIp]++

		if DEBUG {
			fmt.Print("ip=", registers[ip], "\t", registers, "\t\t")
			printInstr(next_instruction)
			fmt.Print("\t")
		}

		op := next_instruction[0]
		arg1 := next_instruction[1]
		arg2 := next_instruction[2]
		arg3 := next_instruction[3]

		/* define the reading sources */
		switch op {
		case OP_ADDR, OP_MULR, OP_BANR, OP_BORR:
			from[0] = 'r'
			from[1] = 'r'
		case OP_GTIR, OP_EQIR:
			from[1] = 'r'
		case OP_GTRI, OP_EQRI, OP_SETR, OP_ADDI, OP_MULI, OP_BANI, OP_BORI:
			from[0] = 'r'
		case OP_GTRR, OP_EQRR:
			from[0] = 'r'
			from[1] = 'r'
		}

		if from[0] == 'r' {
			arg1 = registers[arg1]
		}
		if from[1] == 'r' {
			arg2 = registers[arg2]
		}

		switch op {
		case OP_ADDR, OP_ADDI:
			registers[arg3] = arg1 + arg2
		case OP_MULI, OP_MULR:
			registers[arg3] = arg1 * arg2
		case OP_BANI, OP_BANR:
			registers[arg3] = arg1 & arg2
		case OP_BORI, OP_BORR:
			registers[arg3] = arg1 | arg2
		case OP_GTIR, OP_GTRI, OP_GTRR:
			if arg1 > arg2 {
				registers[arg3] = 1
			} else {
				registers[arg3] = 0
			}
		case OP_EQRR, OP_EQIR, OP_EQRI:
			if arg1 == arg2 {
				registers[arg3] = 1
			} else {
				registers[arg3] = 0
			}
		case OP_SETI, OP_SETR:
			registers[arg3] = arg1
		}

		if DEBUG {
			fmt.Println("", registers)
		}

		registers[ip]++

		if registers[ip] == breakPoint {
			return
		}

	}
}

func main() {
	load_program("input.txt")

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	go func() {
		<-c
		printProgram()
		os.Exit(1)
	}()

	lastSeen := -1
	seen := make(map[int]bool)

	for {
		execute_program(28)

		if lastSeen == -1 {
			fmt.Println("part1:", registers[4])
		}

		if _, found := seen[registers[4]]; found {
			fmt.Println("part2:", lastSeen)
			break
		}

		lastSeen = registers[4]
		seen[registers[4]] = true
	}
}
