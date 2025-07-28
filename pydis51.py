# Author: SYEED MOHD AMEEN                                    Dated: 28/07/2025                                   
# webpage: https://syeedameen.github.io/  
# License: GPLv3 



# TODO: 
#       1. add output assembly file generating function)
#       2. build a test case of all the instrucitons and generate hex file
#       3. add some matrix about hex code like opcode (0x00 - 0xff) histogram, instruction by there occurance 
#          frequencies MOV A, R1 = 45



import intelhex as h                # intel hex file manipulation 
import math as m                    # mathematics library 
import table as t                   # instruction memonics defined here 
import os                           # operating system 
import re                           # regular experession 
import sys                  
# import matplotlib.pyplot as plt     # for ploating instructions distribution histogram


version = """
    dis51  v1.0.0 (first stable release)
    Target: python 3.x        
"""

help = """
    PYTHON DISASSEMBLER THAT CONVERT INTEL HEX FILE INTO 8051 ASSEMBLY INSTRUCTIONS
    
    Author: SYEED MOHD AMEEN 
    repository: https://github.com/syeedameen/pydeasm
    report bug: ameensyeed2001@gmail.com 


dis51 [INPUT_HEX_FILE], [OUTPUT_ASM_FILE], Commands..... 


Commands:
	-d                      : Dump the content 
	-m <args>               : Show assembly matrix 
    \t <his> = histogram of instructions 
    \t <ins> = instructions distribution 
    -v | -version               : Show the current release build version
    -h | -help | --help         : Show the help 


Internal Commands:
	r - rebuild disassembly [development tool]
	R - rebuild disassembly and clean overlapping locations [development tool]

"""



# some constants defined here 
accumulator         = 0 
reg                 = 1
i_reg               = 2 
page_address        = 3 
address_16_bit      = 4 
data_16_bit         = 5 
bit_address         = 7 
relative_address    = 8 
iram_address        = 9 
carry               = 10 
immediate_data      = 11 
i_acc_pl_dptr       = 12 
i_acc_pl_pc         = 13
i_dptr              = 14
Breg                = 15 
dptr                = 16 
comp_bit_address    = 17 

NAME = 0 
LEN = 1 
ARG1 = 2 
ARG2  = 3 
JMP = 4 
COND_JMP = 5 

ADDR16 = 1
ADDR11 = 2 
DIRECT = 3 
BIT = 4 
OFFSET = 5 
IMMED = 6 
A = 7 
IR0 = 8 
IR1 = 9 
R0 = 10 
R1 = 11 
R2 = 12 
R3 = 13 
R4 = 14 
R5 = 15 
R6 = 16 
R7 = 17 
IMMED16 = 18  
C = 19 

map_dict = {A:"A", IR0:"R0", IR1:"R1", R0:"R0", 
            R1:"R1", R2:"R2", R3:"R3", R4:"R4", 
            R5:"R5", R6:"R6", R7:"R7"
            }

# list of all the MCS-51 instructions and it's decoding 
instruction_8051 = [

#   name  len  arg1  arg1  jmp   cond-jmp
    ["NOP", 1, None, None, False, False],
    ["AJMP ", 2, ADDR11, None, True, False],
    ["LJMP ", 3, ADDR16, None, True, False],
    ["RR A", 1, None, None, False, False],
    ["INC A", 1, None, None, False, False],
    ["INC ", 2, DIRECT, None, False, False],
    ["INC @R0", 1, None, None, False, False],
    ["INC @R1", 1, None, None, False, False],
    ["INC R0", 1, None, None, False, False],
    ["INC R1", 1, None, None, False, False],
    ["INC R2", 1, None, None, False, False],
    ["INC R3", 1, None, None, False, False],
    ["INC R4", 1, None, None, False, False],
    ["INC R5", 1, None, None, False, False],
    ["INC R6", 1, None, None, False, False],
    ["INC R7", 1, None, None, False, False],      # 0xFF
    ["JBC ", 3, BIT, OFFSET, False, True],
    ["ACALL ", 2, ADDR11, None, False, True],
    ["LCALL ", 3, ADDR16, None, False, True],
    ["RRC A", 1, None, None, False, False],
    ["DEC A", 1, None, None, False, False],
    ["DEC ", 2, DIRECT, None, False, False],
    ["DEC @R0", 1, None, None, False, False],
    ["DEC @R1", 1, None, None, False, False],
    ["DEC R0", 1, None, None, False, False],
    ["DEC R1", 1, None, None, False, False],
    ["DEC R2", 1, None, None, False, False],
    ["DEC R3", 1, None, None, False, False],
    ["DEC R4", 1, None, None, False, False],
    ["DEC R5", 1, None, None, False, False],
    ["DEC R6", 1, None, None, False, False],
    ["DEC R7", 1, None, None, False, False],   # 0x1F
    ["JB ", 3, BIT, OFFSET, False, True],
    ["AJMP ", 2, ADDR11, None, True, False],
    ["RET", 1, None, None, False, False],
    ["RL A", 1, None, None, False, False],    
    ["ADD A, ", 2, IMMED, None, False, False],
    ["ADD A, ", 2, DIRECT, None, False, False],
    ["ADD A, @R0", 1, None, None, False, False],
    ["ADD A, @R1", 1, None, None, False, False],
    ["ADD A, R0", 1, None, None, False, False],
    ["ADD A, R1", 1, None, None, False, False],
    ["ADD A, R2", 1, None, None, False, False],
    ["ADD A, R3", 1, None, None, False, False],
    ["ADD A, R4", 1, None, None, False, False],
    ["ADD A, R5", 1, None, None, False, False],
    ["ADD A, R6", 1, None, None, False, False],
    ["ADD A, R7", 1, None, None, False, False],   #0x2F
    ["JNB ", 3, BIT, OFFSET, False, True],
    ["ACALL ", 2, ADDR11, None, False, True],
    ["RETI", 1, None, None, False, False],
    ["RLC A", 1, None, None, False, False],
    ["ADDC A, ", 2, IMMED, None, False, False],
    ["ADDC A, ", 2, DIRECT, None, False, False],
    ["ADDC A, @R0", 1, None, None, False, False],
    ["ADDC A, @R1", 1, None, None, False, False],
    ["ADDC A, R0", 1, None, None, False, False],
    ["ADDC A, R1", 1, None, None, False, False],
    ["ADDC A, R2", 1, None, None, False, False],
    ["ADDC A, R3", 1, None, None, False, False],
    ["ADDC A, R4", 1, None, None, False, False],
    ["ADDC A, R5", 1, None, None, False, False],
    ["ADDC A, R6", 1, None, None, False, False],
    ["ADDC A, R7", 1, None, None, False, False],   #0x3F
    ["JC ", 2, OFFSET, None, False, True],
    ["AJMP ", 2, ADDR11, None, True, False],
    ["ORL ", 2, DIRECT, A, False, False],
    ["ORL ", 3, DIRECT, IMMED, False, False],
    ["ORL A, ", 2, IMMED, None, False, False],
    ["ORL A, ", 2, DIRECT, None, False, False],
    ["ORL A, @R0", 1, None, None, False, False],
    ["ORL A, @R1", 1, None, None, False, False],
    ["ORL A, R0", 1, None, None, False, False],
    ["ORL A, R1", 1, None, None, False, False],
    ["ORL A, R2", 1, None, None, False, False],
    ["ORL A, R3", 1, None, None, False, False],
    ["ORL A, R4", 1, None, None, False, False],
    ["ORL A, R5", 1, None, None, False, False],
    ["ORL A, R6", 1, None, None, False, False],
    ["ORL A, R7", 1, None, None, False, False],    #0x4F
    ["JNC ", 2, OFFSET, None, False, True],    
    ["ACALL ", 2, ADDR11, None, False, True],
    ["ANL ", 2, DIRECT, A, False, False],
    ["ANL ", 3, DIRECT, IMMED, False, False],
    ["ANL A, ", 2, IMMED, None, False, False],
    ["ANL A, ", 2, DIRECT, None, False, False],
    ["ANL A, @R0", 1, None, None, False, False],
    ["ANL A, @R1", 1, None, None, False, False],
    ["ANL A, R0", 1, None, None, False, False],
    ["ANL A, R1", 1, None, None, False, False],
    ["ANL A, R2", 1, None, None, False, False],
    ["ANL A, R3", 1, None, None, False, False],
    ["ANL A, R4", 1, None, None, False, False],
    ["ANL A, R5", 1, None, None, False, False],
    ["ANL A, R6", 1, None, None, False, False],
    ["ANL A, R7", 1, None, None, False, False],    #0x5F
    ["JZ ", 2, OFFSET, None, False, True],
    ["AJMP ", 2, ADDR11, None, True, False],
    ["XRL ", 2, DIRECT, A, False, False],
    ["XRL ", 3, DIRECT, IMMED, False, False],
    ["XRL A, ", 2, IMMED, None, False, False],
    ["XRL A, ", 2, DIRECT, None, False, False],
    ["XRL A, @R0", 1, None, None, False, False],
    ["XRL A, @R1", 1, None, None, False, False],
    ["XRL A, R0", 1, None, None, False, False],
    ["XRL A, R1", 1, None, None, False, False],
    ["XRL A, R2", 1, None, None, False, False],
    ["XRL A, R3", 1, None, None, False, False],
    ["XRL A, R4", 1, None, None, False, False],
    ["XRL A, R5", 1, None, None, False, False],
    ["XRL A, R6", 1, None, None, False, False],
    ["XRL A, R7", 1, None, None, False, False],  #0x6F
    ["JNZ ", 2, OFFSET, None, False, True],
    ["ACALL ", 2, ADDR11, None, False, True],
    ["ORL C, ", 2, BIT, None, False, False],
    ["JMP @A+DPTR", 1, None, None, False, False], 
    ["MOV A, ", 2, IMMED, None, False, False],
    ["MOV ", 3, DIRECT, IMMED, False, False],
    ["MOV @R0, ", 2, IMMED, None, False, False],
    ["MOV @R1, ", 2, IMMED, None, False, False],
    ["MOV R0, ", 2, IMMED, None, False, False],
    ["MOV R1, ", 2, IMMED, None, False, False],
    ["MOV R2, ", 2, IMMED, None, False, False],
    ["MOV R3, ", 2, IMMED, None, False, False],
    ["MOV R4, ", 2, IMMED, None, False, False],
    ["MOV R5, ", 2, IMMED, None, False, False],
    ["MOV R6, ", 2, IMMED, None, False, False],
    ["MOV R7, ", 2, IMMED, None, False, False],  #0x7F
    ["SJMP ", 2, OFFSET, None, True, False],
    ["AJMP ", 2, ADDR11, None, True, False],
    ["ANL C, ", 2, BIT, None, False, False],
    ["MOVC A, @A+PC", 1, None, None, False, False],
    ["DIV AB", 1, None, None, False, False],
    ["MOV ", 3, DIRECT, DIRECT, False, False],  
    ["MOV ", 2, DIRECT, IR0, False, False],
    ["MOV ", 2, DIRECT, IR1, False, False],
    ["MOV ", 2, DIRECT, R0, False, False],
    ["MOV ", 2, DIRECT, R1, False, False],
    ["MOV ", 2, DIRECT, R2, False, False],
    ["MOV ", 2, DIRECT, R3, False, False],
    ["MOV ", 2, DIRECT, R4, False, False],
    ["MOV ", 2, DIRECT, R5, False, False],
    ["MOV ", 2, DIRECT, R6, False, False],
    ["MOV ", 2, DIRECT, R7, False, False],              #0x8F
    ["MOV DPTR, ", 3, IMMED16, None, False, False],
    ["ACALL ", 2, ADDR11, None, False, True],
    ["MOV ", 2, BIT, C, False, False],
    ["MOVC A, @A+DPTR", 1, None, None, False, False],
    ["SUBB A, ", 2, IMMED, None, False, False],
    ["SUBB A, ", 2, DIRECT, None, False, False],
    ["SUBB A, @R0", 1, None, None, False, False],
    ["SUBB A, @R1", 1, None, None, False, False],
    ["SUBB A, R0", 1, None, None, False, False],
    ["SUBB A, R1", 1, None, None, False, False],
    ["SUBB A, R2", 1, None, None, False, False],
    ["SUBB A, R3", 1, None, None, False, False],
    ["SUBB A, R4", 1, None, None, False, False],
    ["SUBB A, R5", 1, None, None, False, False],
    ["SUBB A, R6", 1, None, None, False, False],
    ["SUBB A, R7", 1, None, None, False, False],        #0x9F
    ["ORL C, ", 2, BIT, None, False, False],
    ["AJMP ", 2, ADDR11, None, True, False],
    ["MOV C, ", 2, BIT, None, False, False],
    ["INC DPTR", 1, None, None, False, False],
    ["MUL AB", 1, None, None, False, False],
    ["RESERVED", 1, None, None, False, False],
    ["MOV @R0, ", 2, DIRECT, None, False, False],
    ["MOV @R1, ", 2, DIRECT, None, False, False],
    ["MOV R0, ", 2, DIRECT, None, False, False],
    ["MOV R1, ", 2, DIRECT, None, False, False],
    ["MOV R2, ", 2, DIRECT, None, False, False],
    ["MOV R3, ", 2, DIRECT, None, False, False],
    ["MOV R4, ", 2, DIRECT, None, False, False],
    ["MOV R5, ", 2, DIRECT, None, False, False],
    ["MOV R6, ", 2, DIRECT, None, False, False],
    ["MOV R7, ", 2, DIRECT, None, False, False],        #0xAF
    ["ANL C, ", 2, BIT, None, False, False],
    ["ACALL ", 2, ADDR11, None, False, True],
    ["CPL ", 2, BIT, None, False, False],
    ["CPL C", 1, None, None, False, False],
    ["CJNE A, ", 3, IMMED, OFFSET, False, True],
    ["CJNE A, ", 3, DIRECT, OFFSET, False, True],
    ["CJNE @R0, ", 3, IMMED, OFFSET, False, True],
    ["CJNE @R1, ", 3, IMMED, OFFSET, False, True],
    ["CJNE R0, ", 3, IMMED, OFFSET, False, True],
    ["CJNE R1, ", 3, IMMED, OFFSET, False, True],
    ["CJNE R2, ", 3, IMMED, OFFSET, False, True],
    ["CJNE R3, ", 3, IMMED, OFFSET, False, True],
    ["CJNE R4, ", 3, IMMED, OFFSET, False, True],
    ["CJNE R5, ", 3, IMMED, OFFSET, False, True],
    ["CJNE R6, ", 3, IMMED, OFFSET, False, True],
    ["CJNE R7, ", 3, IMMED, OFFSET, False, True],       #0xBF
    ["PUSH ", 2, DIRECT, None, False, False],
    ["AJMP ", 2, ADDR11, None, True, False],
    ["CLR ", 2, BIT, None, False, False],
    ["CLR C", 1, None, None, False, False],
    ["SWAP A", 1, None, None, False, False],
    ["XCH A, ", 2, DIRECT, None, False, False],
    ["XCH A, @R0", 1, None, None, False, False],
    ["XCH A, @R1", 1, None, None, False, False],
    ["XCH A, R0", 1, None, None, False, False],
    ["XCH A, R1", 1, None, None, False, False],
    ["XCH A, R2", 1, None, None, False, False],
    ["XCH A, R3", 1, None, None, False, False],
    ["XCH A, R4", 1, None, None, False, False],
    ["XCH A, R5", 1, None, None, False, False],
    ["XCH A, R6", 1, None, None, False, False],
    ["XCH A, R7", 1, None, None, False, False],         #0xCF
    ["POP ", 2, DIRECT, None, False, False],
    ["ACALL ", 2, ADDR11, None, False, True],
    ["SETB ", 2, BIT, None, False, False],
    ["SETB C", 1, None, None, False, False],
    ["DA A", 1, None, None, False, False],
    ["DJNZ ", 3, DIRECT, OFFSET, False, True],
    ["XCHD A, @R0", 1, None, None, False, False],
    ["XCHD A, @R1", 1, None, None, False, False],
    ["DJNZ R0, ", 2, OFFSET, None, False, True],
    ["DJNZ R1, ", 2, OFFSET, None, False, True],
    ["DJNZ R2, ", 2, OFFSET, None, False, True],
    ["DJNZ R3, ", 2, OFFSET, None, False, True],
    ["DJNZ R4, ", 2, OFFSET, None, False, True],
    ["DJNZ R5, ", 2, OFFSET, None, False, True],
    ["DJNZ R6, ", 2, OFFSET, None, False, True],
    ["DJNZ R7, ", 2, OFFSET, None, False, True],       #0xDF
    ["MOVX A, @DPTR", 1, None, None, False, False],
    ["AJMP ", 2, ADDR11, None, True, False],
    ["MOVX, A, @R0", 1, None, None, False, False],
    ["MOVX, A, @R1", 1, None, None, False, False],
    ["CLR A", 1, None, None, False, False],
    ["MOV A, ", 2, DIRECT, None, False, False],
    ["MOV A, @R0", 1, None, None, False, False],
    ["MOV A, @R1", 1, None, None, False, False],
    ["MOV A, R0", 1, None, None, False, False],
    ["MOV A, R1", 1, None, None, False, False],
    ["MOV A, R2", 1, None, None, False, False],
    ["MOV A, R3", 1, None, None, False, False],
    ["MOV A, R4", 1, None, None, False, False],
    ["MOV A, R5", 1, None, None, False, False],
    ["MOV A, R6", 1, None, None, False, False],
    ["MOV A, R7", 1, None, None, False, False],             #0xEF
    ["MOVX @DPTR, A", 1, None, None, False, False],
    ["ACALL ", 2, ADDR11, None, False, True],
    ["MOVX @R0, A", 1, None, None, False, False],
    ["MOVX @R1, A", 1, None, None, False, False],
    ["CPL A", 1, None, None, False, False],
    ["MOV ", 2, DIRECT, A, False, False],
    ["MOV @R0, A", 1, None, None, False, False],
    ["MOV @R1, A", 1, None, None, False, False],
    ["MOV R0, A", 1, None, None, False, False],
    ["MOV R1, A", 1, None, None, False, False],
    ["MOV R2, A", 1, None, None, False, False],
    ["MOV R3, A", 1, None, None, False, False],
    ["MOV R4, A", 1, None, None, False, False],
    ["MOV R5, A", 1, None, None, False, False],
    ["MOV R6, A", 1, None, None, False, False],
    ["MOV R7, A", 1, None, None, False, False]              #0xFF
]

# special function register naming. 
SFR = [

    # special function registers defined 0x80 - 0xFF upper bank of 128 bytes of memory
    "P0", "SP","DPL","DPH","x84","x85","x86","PCON",                        #80-87
    "TCON", "TMOD","TL0","TL1","TH0","TH1","CKCON","PSCTL",                 #88-8F
    "P1", "x91","LINADDR","LINDATA","x94","LINCF","x96","x97",              #90-87
    "SCON", "SBUF","x9A","CPTCN","x9C","CPTMD","x9E","CPTMX",               #98-8F
    "xA0", "SPICFG","SPICKR","SPIDAT","P0MDOUT","P1MDOUT","x86","x87",      #A0-A7
    "IE", "CLKSEL","xAA","xAB","xAC","xAD","xAE","xAF",                     #A8-AF
    "OSCIFIN", "OSCXCN","OSCICN","OSCICL","xB4","xB5","xB6","FLKEY",        #B0-B7
    "IP", "xB9","ADCTK","ADCMX","ADCCF","ADCL","ADC","P1MASK",              #B8-BF
    "xC0", "xC1","xC2","ADCGTL","ADCGTH","ADCLTL","ADCLTH","P0MASK",        #C0-C7
    "TMP2CN", "REGCN","TMR2RLL","TMR2RLH","TMP2L","TMR2H","x8E","P1MAT",    #C8-CF
    "PSW", "REFCN","xD2","xD3","P0SKIP","P1SKIP","xD6","P0MAT",             #D0-D7
    "PCACN", "PCAMD","PCACPM0","PCACPM1","PCACPM2","xDD","xDE","xDF",       #D8-DF
    "ACC", "XBR0","XBR1","xE3","IT01CF","xE5","EIE1","xE7",                 #E0-E7
    "ADCCN", "PCACPL1","PCACPH1","PCACPL2","PCACPH2","xED","xEE","RSTSRC",  #E8-EF
    "B", "P0MDIN","P1MDIN","xF3","xF4","xF5","EIP1","xF7",                  #F0-F7
    "SPICN", "PCAL","PCAH","PCACPL0","PCACPH0","xFD","xFE","VDDMON"         #F8-FF
]

# Bit map for special function registers 
BIT_MAP = [   

  # bit map start with 0x80; less then 0x80 is general purpose use
  "P0_0", "P0_1", "P0_2", "P0_3", "P0_4", "P0_5", "P0_6", "P0_7",         # P0    (0x80)
  "IT0", "IE0", "IT1", "IE1", "TR0", "TF0", "TR1", "TF1",                 # TCON  (0x88)
  "P1_0", "P1_1", "P1_2", "P1_3", "P1_4", "P1_5", "P1_6", "P1_7",         # P1    (0x90)
  "RI_0", "TI_0", "RB8_0", "TB8_0", "REN_0", "SM2_0", "SM1_0", "SM0_0",   # SCON0 (0x98)
  "P2_0", "P2_1", "P2_2", "P2_3", "P2_4", "P2_5", "P2_6", "P2_7",         # P2    (0xA0)
  "EX0", "ET0", "EX1", "ET1", "ES0", "ET2", "ES1", "EA",                  # IE    (0xA8) 
  "P3_0", "P3_1", "P3_2", "P3_3", "P3_4", "P3_5", "P3_6", "P3_7",         # P3    (0xB0)
  "LPX0", "LPT0", "LPX1", "LPT1", "LPS0", "LPT2", "LPS1", "0xBF",         # IP0   (0xB8)
  "RI_1", "TI_1", "RB8_1", "TB8_1", "REN_1", "SM2_1", "SM1_1", "SM0_1",   # SCON1 (0xC0)
  "CP_RL_2", "C_T_2", "TR_2", "EXEN_2", "TCLK", "RCLK", "EXF_2", "TF_2",  # T2CON (0xC8)
  "PARITY", "F1", "OV", "RS0", "RS1", "F0", "AC", "CY",                   # PSW   (0xD0)
  "RWT", "EWT", "WTRF", "WDIF", "PFI", "EPFI", "POR", "SMOD_1",           # WDCON (0xD8)
  "0xE0", "0xE1", "0xE2", "0xE3", "0xE4", "0xE5", "0xE6", "0xE7",         # None  (0xE0)
  "EX2", "EX3", "EX4", "EX5", "EWDI", "0xED",   "0xEE",   "0xEF",         # EIE   (0xE8) 
  "F0h", "F1h", "F2h", "F3h", "F4h", "F5h", "F6h", "F7h",                 # None  (0xF0)
  "LPX2", "LPX3", "LPX4", "LPX5", "LPWDI", "0xFD", "0xFE", "0xFF"         # EIP0  (0xF8)
]



# TODO : add all the instruction with there calssification 
# list of list that hold types of computer instructions (for analysis purposes)
types_of_instructions = [
    [],                                 # arithmetic instructions 
    [],                                 # logical instructions
    [],                                 # data transfer instructions
    [],                                 # boolean variable manipulations
    [],                                 # Program branching instructions
]




l = [] 
address = []                        # list of all the address of hex file 
memoryData = []                     # list of all the memory data(opcode) of hex file 
PC = 0                              # program counter (keep track the hex opcode) 
space = 0                       
line = 0
dump = False                        # flag for dump the content on terminal 
input_file = None                   # input hex file 
output_file = None                  # output asm file 

# formatted hex function 
def hex2(n):
    return "0x" + hex(n)[2:].zfill(2)


"""
- function that will convert the intel hex file into address and its correpondand memory data 
"""
def create_array():
    global PC
    global space 
    global line 
    global d 

    for i in d:
        address.append(hex(i))
    for i in d:
        memoryData.append(hex(d[i]))

    # # write the array into the file location 
    # fa.write("const int address[] = { \n")
    # for i in address:
    #     space += 1 
    #     PC += 1 
    #     line += 1 

    #     fa.write(i)
    #     if (PC == len(address)):
    #         break
    #     fa.write(",")

    #     if (space == 8):
    #         fa.write(" ")
    #         space = 0 
    #     if (line == 16):
    #         fa.write("\n")
    #         line = 0
    # fa.write("};")

    # fa.write("\n \n \n \n \n")          # give some sapce in memory and data array 
    # PC = 0                              # reset all the values 
    # space = 0 
    # line = 0


    # # write the array of memory data into the file location 
    # fa.write("const byte data[] = {\n")
    # for i in memoryData:
    #     space += 1 
    #     PC += 1 
    #     line += 1 

    #     fa.write(i)
    #     if (PC == len(memoryData)):
    #         break
    #     fa.write(",")

    #     if (space == 8):
    #         fa.write(" ")
    #         space = 0 
    #     if (line == 16):
    #         fa.write("\n")
    #         line = 0
    # fa.write("};")



# function to decode the command line arguments 
def decode():
    counter = 0 
    l =  []                     # list of argument
    global input_file
    global output_file
    global dump 

    for i in sys.argv:
        l.append(i)
        counter += 1 
    # # at the end append the number of argumenst into the list 
    # l.append(counter)

    # if found any of the below string in the comamnd line argument 
    if ("--help" in l) or ("-help" in l) or ("-h" in l):
        print(help)
        exit()                                              # interrupt the execution; sys call 
    
    # if found any of the below string in the command line argument 
    if ("-v" in l) or ("-version" in l):
        print(version)
        exit()

    # if -d flag present dump the content of hex file. 
    if ("-d") in l:         
        dump = True
    
    # match input hex file ending with .hex extention.
    pattern = r'.*\.hex$'
    for file in l:
        if re.match(pattern, file, re.IGNORECASE):
            input_file = file
            break
    
    # match output asm file ending with .asm extention. 
    pattern = r'.*\.asm'
    for file in l:
        if re.match(pattern, file, re.IGNORECASE):
            output_file = file
            break

decode()                            # call decode function to decode command line arguments 
ih = h.IntelHex()                   # input hex file

# see the output file 
if output_file != None:
    fd = open(output_file, "w+")       # output assembly file generated
else:
    print("Error : output file")
    exit()                              # interrupt the execution; sys call 

# see the input file 
if input_file != None:    
    ih.loadhex(input_file) 
else:
    print("Error : input file not found ")
    exit()                              # interrupt the execution; sys call 


fa = open("array.txt", "w+")        # second file to convert into array of data 
d = ih.todict()                     # hex file to set of address. 
create_array()                      # create array of address and data memory 



# disassembler program start here
program_size = len(memoryData)
program_counter = 0 
temp = []

# TODO : add instruction distribution matric as well (memory instruction, arithmetic, logication etc.)
# opcode histogram list (nubmer of opcodes) 
opcode_hist = [] 
# add opcode histogram data into the list 
for i in range(0, 1025):
    opcode_hist.append(0)

for i in memoryData:  
    opcode_hist[int(i, 16)] += 1    # increment particular instruction 

# print("Instruction distribution :", opcode_hist)
# append all the instruction related to move and data transfer 


# iterate the loop until we parse the whole hex file 
while (program_counter < program_size):
    current_instruction = int(memoryData[program_counter], 16)
   

    # handling one byte instructions
    if (instruction_8051[current_instruction][LEN] == 1):
        temp.append(int(memoryData[program_counter], 16))

        if dump == True:
            print(f"{program_counter:04x}   ", "(",f'{temp[0]:02x}', ")", "       :       ", end="", sep="")                        
            print(instruction_8051[current_instruction][NAME])
        t = "{ADDRESS}\t ({OPCODE}) \t\t : {MEMONICS}\n".format(ADDRESS = f'{program_counter:04x}', OPCODE = f'{temp[0]:02x}', MEMONICS = instruction_8051[current_instruction][NAME])
        fd.writelines(t)
        temp.clear()
        

    # handling two byte instructions with different addressing modes 
    elif (instruction_8051[current_instruction][LEN] == 2):
        temp.append(int(memoryData[program_counter], 16))
        temp.append(int(memoryData[program_counter + 1], 16))
        if dump == True:
            print(f"{program_counter:04x}   ", "(", f'{temp[0]:02x}', ", ", f'{temp[1]:02x}', ")", "   :       ", end="", sep="")
        t = "{ADDRESS}\t ({OPCODE1} {OPCODE2}) \t : ".format(ADDRESS = f'{program_counter:04x}', OPCODE1 = f'{temp[0]:02x}', OPCODE2 = F'{temp[1]:02x}')
        fd.writelines(t)
        temp.clear()
        

        # handling direct address instructions 
        if ((instruction_8051[current_instruction][ARG1] == DIRECT) and (instruction_8051[current_instruction][ARG2] == None)):
            value = int(memoryData[program_counter + 1], 16)
            if (value > 0x80):
                if dump == True:
                    print(instruction_8051[current_instruction][0], SFR[int(memoryData[program_counter + 1],16) - 0x80], sep="")
                t = "{MEMONICS} {SFR_REG}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], SFR_REG = SFR[int(memoryData[program_counter + 1],16) - 0x80])
                fd.writelines(t)
            else:
                if dump == True:
                    print(instruction_8051[current_instruction][0], memoryData[program_counter + 1], sep="")
                t = "{MEMONICS} {SFR_DIRECT}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], SFR_DIRECT = memoryData[program_counter + 1])
                fd.writelines(t)
            program_counter += 1 

        
        # handling immediate address instructions with 8-bit immediate value (In two byte instructions)
        elif (instruction_8051[current_instruction][ARG1] == IMMED):
            if dump == True:
                print(instruction_8051[current_instruction][0], "#",memoryData[program_counter + 1], sep="")
            t = "{MEMONICS} #{IMMEDIATE_VALUE}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], IMMEDIATE_VALUE = memoryData[program_counter + 1])
            fd.writelines(t)
            program_counter += 1 


        # handling instruction that's have destination one byte address 
        elif((instruction_8051[current_instruction][ARG1]) and (instruction_8051[current_instruction][ARG2] != None)):
            if dump == True:
                print(instruction_8051[current_instruction][0], memoryData[program_counter + 1], ",", map_dict[instruction_8051[current_instruction][ARG2]], sep="")
            t = "{MEMONICS} {DIRECT_ADDR}, {SECOND_ARG}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], DIRECT_ADDR = memoryData[program_counter + 1], SECOND_ARG = map_dict[instruction_8051[current_instruction][ARG2]])
            fd.writelines(t)
            program_counter += 1
        

        # handling 11-bit absolute address instructions 
        elif (instruction_8051[current_instruction][ARG1] == ADDR11):
            value = int(memoryData[program_counter + 1], 16)
            value = value | (((int(memoryData[program_counter], 16) >> 5) & 7) << 8)   # calculate the 11-bit absolute address using bit masking  
            program_counter += 1 
            if dump == True:
                print(instruction_8051[current_instruction][0], hex(value), sep="")
            t = "{MEMONICS} {ADDR_11}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], ADDR_11 = hex(value))
            fd.writelines(t)
            

        # handling relative 8 - bit offset address instructions 
        elif (instruction_8051[current_instruction][ARG1] == OFFSET):
            value = int(memoryData[program_counter+1], 16)
            value += program_counter + 2
            program_counter += 1
            if dump == True:
                print(instruction_8051[current_instruction][0], hex(value), sep="")
            t = "{MEMONICS} {RELATIVE_ADDR}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], RELATIVE_ADDR = hex(value))
            fd.writelines(t)
            

        # handling bit addressing mode instruction 
        elif (instruction_8051[current_instruction][ARG1] == BIT):
            value = int(memoryData[program_counter + 1], 16)
            program_counter += 1
            if value > 0x80:
                if dump == True:
                    print(instruction_8051[current_instruction][0], BIT_MAP[value - 0x80])
                t = "{MEMONICS} {BIT_VALUE}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], BIT_VALUE = BIT_MAP[value - 0x80])
                fd.writelines(t)
            else:
                if dump == True:
                    print(instruction_8051[current_instruction][0], hex(value))
                t = "{MEMONICS} {BIT_VALUE}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], BIT_VALUE = hex(value))
                fd.writelines(t)
                        

    # handling three byte instructions with different addressing modes 
    else:
        if dump == True:
            print(f"{program_counter:04x}", "  ", end="")
        temp.append(int(memoryData[program_counter], 16))
        temp.append(int(memoryData[program_counter + 1], 16))
        temp.append(int(memoryData[program_counter + 2], 16))

        if dump == True:
            print("(", f'{temp[0]:02x}', ", ", f'{temp[1]:02x}', ",", f'{temp[2]:02x}', ")", ":       ", end="", sep="")
        t = "{ADDRESS}\t ({OPCODE1} {OPCODE2} {OPCODE3})  : ".format(ADDRESS = f'{program_counter:04x}', OPCODE1 = f'{temp[0]:02x}', OPCODE2 = f'{temp[1]:02x}', OPCODE3 = f'{temp[2]:02x}')
        fd.writelines(t)
        temp.clear()
        

        # handling 16-direct address instructions 
        if(instruction_8051[current_instruction][ARG1] == ADDR16):
            imm_value_h = int(memoryData[program_counter + 1], 16)
            imm_value_l = int(memoryData[program_counter + 2], 16)
            program_counter += 2 
            if dump == True:
                print(instruction_8051[current_instruction][0], ",", hex(imm_value_h), hex(imm_value_l), sep="")
            t = "{MEMONICS} {ADDR_16_HIGH}{ADDR_16_LOW}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], ADDR_16_HIGH = hex(imm_value_h), ADDR_16_LOW = hex(imm_value_l))
            fd.writelines(t)
              

        # handling 16-bit Immediate value instructions 
        elif (instruction_8051[current_instruction][ARG1] == IMMED16):
            imm_value_h = int(memoryData[program_counter + 1], 16)
            imm_value_l = int(memoryData[program_counter + 2], 16)
            program_counter += 2
            if dump == True:
                print(instruction_8051[current_instruction][0], ",", "#", hex(imm_value_h), hex(imm_value_l), sep="")
            t = "{MEMONICS}, #{ADDR_16_HIGH}{ADDR_16_LOW}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], ADDR_16_HIGH = hex(imm_value_h), ADDR_16_LOW = hex(imm_value_l))
            fd.writelines(t)


        # handling jump instruction based on bit value 
        elif (instruction_8051[current_instruction][ARG1] == BIT):
            bit_value = int(memoryData[program_counter + 1], 16)
            rel_addr  = int(memoryData[program_counter + 2], 16)
            rel_addr = rel_addr + program_counter + 2
            program_counter += 2 
            if dump == True:
                print(instruction_8051[current_instruction][0], hex(bit_value), ",", hex(rel_addr),sep="")
            t = "{MEMONICS} {BIT_VALUE}, {RELATIVE_ADDR}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], BIT_VALUE = hex(bit_value), RELATIVE_ADDR = hex(rel_addr))
            fd.writelines(t)

        
        # hadling (moving immediate value to a direct 8-bit address)
        elif (instruction_8051[current_instruction][ARG1] == DIRECT):
            direct_addr = int(memoryData[program_counter + 1], 16)
            imm_value   = int(memoryData[program_counter + 2], 16)
            program_counter += 2 
            
            # convert the direct address into special function registers (SFR)
            if (direct_addr > 0x80):
                direct_addr = SFR[direct_addr - 0x80]
                if dump == True:
                    print(instruction_8051[current_instruction][0], direct_addr, ",","#", hex(imm_value), sep="")
                t = "{MEMONICS} {DIRECT_ADDR}, #{IMMEDIATE_VALUE}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], DIRECT_ADDR = direct_addr, IMMEDIATE_VALUE = hex(imm_value))
                fd.writelines(t)

            else:
                if dump == True:
                    print(instruction_8051[current_instruction][0], hex(direct_addr), ",","#", hex(imm_value), sep="")
                t = "{MEMONICS} {DIRECT_ADDR}, #{IMMEDIATE_VALUE}\n".format(MEMONICS = instruction_8051[current_instruction][NAME], DIRECT_ADDR = direct_addr, IMMEDIATE_VALUE = hex(imm_value))
                fd.writelines(t)
    
    # increment the program counter register 
    program_counter += 1


# fd.close()
# f = open("Output.asm",'r')
# for i in f.readlines():
#     print(i, end="")


# delete temporary array files  
if os.path.exists('./array.txt'):
    os.remove('./array.txt')
if os.path.exists('./output.txt'):
    os.remove('./output.txt')