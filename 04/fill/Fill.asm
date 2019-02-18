// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(START)
 	@8192
 	D=A

	@i 	//set counter to cycle through
	M=D

	@current 	//set address adder to 0
	M=0

(INPUT)
	@KBD
	D=M 	//get input from keyboard

	@LOOP2
	D; JEQ 	//no key press=white

(LOOP)
	@current 	//get address adder
	D=M

	@SCREEN 	//go to current pixel & set black
	A=A+D
	M=-1

	@END
	0; JMP	//go to end to increment/decrement

(LOOP2)
	@current 	//get address adder
	D=M

	@SCREEN 	//go to current pixel & set white
	A=A+D
	M=0

	@END
	0; JMP	//go to end to increment/decrement

(END)
	@current
	M=M+1	//increment adder go to next screen address

	@i
	M=M-1	//Decrement screen location count

	@i
	D=M

	@START
	D; JEQ	//If at the end of the screen mem, start over

	@INPUT 	//otherwise get next key input
	0; JMP

