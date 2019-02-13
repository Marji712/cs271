// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

   
	@R2
	M=0

 (LOOP)
	@R1
	D=M

	@END
	D;JEQ	//If R1=0 go to end

	@R0
	D=M	//Set D to R0's value 

	@R2
	M=M+D	//Add R0's value to R2
	
	@R1
	M=M-1	//Decrement R1

	@LOOP
	0; JMP	//go to loop	

    (END)
	@END
	0;JMP	//infinite loop