0000	 (d0 7f) 	 : POP  0x7f
0002	 (d0 7e) 	 : POP  0x7e
0004	 (d0 60) 	 : POP  0x60
0006	 (d0 59) 	 : POP  0x59
0008	 (d0 58) 	 : POP  0x58
000a	 (d0 57) 	 : POP  0x57
000c	 (d0 56) 	 : POP  0x56
000e	 (d0 55) 	 : POP  0x55
0010	 (d0 54) 	 : POP  0x54
0012	 (d0 53) 	 : POP  0x53
0014	 (c0 7e) 	 : PUSH  0x7e
0016	 (c0 7f) 	 : PUSH  0x7f
0018	 (11 39) 	 : ACALL  0x39
001a	 (11 4c) 	 : ACALL  0x4c
001c	 (31 3b) 	 : ACALL  0x13b
001e	 (11 00) 	 : ACALL  0x0
0020	 (d0 7f) 	 : POP  0x7f
0022	 (d0 7e) 	 : POP  0x7e
0024	 (e5 49) 	 : MOV A,  0x49
0026	 (c0 e0) 	 : PUSH  ACC
0028	 (e5 50) 	 : MOV A,  0x50
002a	 (c0 e0) 	 : PUSH  ACC
002c	 (e5 51) 	 : MOV A,  0x51
002e	 (c0 e0) 	 : PUSH  ACC
0030	 (e5 52) 	 : MOV A,  0x52
0032	 (c0 e0) 	 : PUSH  ACC
0034	 (c0 7e) 	 : PUSH  0x7e
0036	 (c0 7f) 	 : PUSH  0x7f
0038	 (22) 		 : RET
0039	 (c2 27) 	 : CLR  0x27
003b	 (c2 26) 	 : CLR  0x26
003d	 (e5 60) 	 : MOV A,  0x60
003f	 (30 d7 02)  : JNB  0xd7, 0x43
0042	 (d2 27) 	 : SETB  0x27
0044	 (e5 56) 	 : MOV A,  0x56
0046	 (30 d7 02)  : JNB  0xd7, 0x4a
0049	 (d2 26) 	 : SETB  0x26
004b	 (22) 		 : RET
004c	 (a9 60) 	 : MOV R1,  0x60
004e	 (a8 56) 	 : MOV R0,  0x56
0050	 (e9) 		 : MOV A, R1
0051	 (c3) 		 : CLR C
0052	 (33) 		 : RLC A
0053	 (f9) 		 : MOV R1, A
0054	 (e5 59) 	 : MOV A,  0x59
0056	 (54 80) 	 : ANL A,  #0x80
0058	 (69) 		 : XRL A, R1
0059	 (f5 48) 	 : MOV  0x48, A
005b	 (e8) 		 : MOV A, R0
005c	 (c3) 		 : CLR C
005d	 (33) 		 : RLC A
005e	 (f8) 		 : MOV R0, A
005f	 (e5 55) 	 : MOV A,  0x55
0061	 (54 80) 	 : ANL A,  #0x80
0063	 (68) 		 : XRL A, R0
0064	 (f5 47) 	 : MOV  0x47, A
0066	 (aa 59) 	 : MOV R2,  0x59
0068	 (a9 58) 	 : MOV R1,  0x58
006a	 (a8 57) 	 : MOV R0,  0x57
006c	 (88 25) 	 : MOV  0x25, R0
006e	 (89 26) 	 : MOV  0x26, R1
0070	 (8a 27) 	 : MOV  0x27, R2
0072	 (ea) 		 : MOV A, R2
0073	 (c3) 		 : CLR C
0074	 (33) 		 : RLC A
0075	 (f5 27) 	 : MOV  0x27, A
0077	 (30 21 02)  : JNB  0x21, 0x7b
007a	 (d2 27) 	 : SETB  0x27
007c	 (e9) 		 : MOV A, R1
007d	 (c3) 		 : CLR C
007e	 (33) 		 : RLC A
007f	 (f5 26) 	 : MOV  0x26, A
0081	 (30 22 02)  : JNB  0x22, 0x85
0084	 (d2 26) 	 : SETB  0x26
0086	 (e8) 		 : MOV A, R0
0087	 (c3) 		 : CLR C
0088	 (33) 		 : RLC A
0089	 (f5 25) 	 : MOV  0x25, A
008b	 (85 27 59)  : MOV  39, #0x59
008e	 (85 26 58)  : MOV  38, #0x58
0091	 (85 25 57)  : MOV  37, #0x57
0094	 (aa 55) 	 : MOV R2,  0x55
0096	 (a9 54) 	 : MOV R1,  0x54
0098	 (a8 53) 	 : MOV R0,  0x53
009a	 (88 25) 	 : MOV  0x25, R0
009c	 (89 26) 	 : MOV  0x26, R1
009e	 (8a 27) 	 : MOV  0x27, R2
00a0	 (ea) 		 : MOV A, R2
00a1	 (c3) 		 : CLR C
00a2	 (33) 		 : RLC A
00a3	 (f5 27) 	 : MOV  0x27, A
00a5	 (30 21 02)  : JNB  0x21, 0xa9
00a8	 (d2 27) 	 : SETB  0x27
00aa	 (e9) 		 : MOV A, R1
00ab	 (c3) 		 : CLR C
00ac	 (33) 		 : RLC A
00ad	 (f5 26) 	 : MOV  0x26, A
00af	 (30 22 02)  : JNB  0x22, 0xb3
00b2	 (d2 26) 	 : SETB  0x26
00b4	 (e8) 		 : MOV A, R0
00b5	 (c3) 		 : CLR C
00b6	 (33) 		 : RLC A
00b7	 (f5 25) 	 : MOV  0x25, A
00b9	 (85 27 55)  : MOV  39, #0x55
00bc	 (85 26 54)  : MOV  38, #0x54
00bf	 (85 25 53)  : MOV  37, #0x53
00c2	 (a9 48) 	 : MOV R1,  0x48
00c4	 (a8 47) 	 : MOV R0,  0x47
00c6	 (e9) 		 : MOV A, R1
00c7	 (b5 00 01)  : CJNE A,  0, #0x1
00ca	 (22) 		 : RET
00cb	 (98) 		 : SUBB A, R0
00cc	 (50 38) 	 : JNC  0x106
00ce	 (e8) 		 : MOV A, R0
00cf	 (99) 		 : SUBB A, R1
00d0	 (fb) 		 : MOV R3, A
00d1	 (ac 57) 	 : MOV R4,  0x57
00d3	 (ad 58) 	 : MOV R5,  0x58
00d5	 (ae 59) 	 : MOV R6,  0x59
00d7	 (8c 25) 	 : MOV  0x25, R4
00d9	 (8d 26) 	 : MOV  0x26, R5
00db	 (8e 27) 	 : MOV  0x27, R6
00dd	 (ec) 		 : MOV A, R4
00de	 (c3) 		 : CLR C
00df	 (13) 		 : RRC A
00e0	 (f5 25) 	 : MOV  0x25, A
00e2	 (30 26 02)  : JNB  0x26, 0xe6
00e5	 (d2 22) 	 : SETB  0x22
00e7	 (ed) 		 : MOV A, R5
00e8	 (c3) 		 : CLR C
00e9	 (13) 		 : RRC A
00ea	 (f5 26) 	 : MOV  0x26, A
00ec	 (30 27 02)  : JNB  0x27, 0xf0
00ef	 (d2 21) 	 : SETB  0x21
00f1	 (ee) 		 : MOV A, R6
00f2	 (c3) 		 : CLR C
00f3	 (13) 		 : RRC A
00f4	 (f5 27) 	 : MOV  0x27, A
00f6	 (ac 25) 	 : MOV R4,  0x25
00f8	 (ad 26) 	 : MOV R5,  0x26
00fa	 (ae 27) 	 : MOV R6,  0x27
00fc	 (db df) 	 : DJNZ R3,  0x1dd
00fe	 (8c 57) 	 : MOV  0x57, R4
0100	 (8d 58) 	 : MOV  0x58, R5
0102	 (8e 59) 	 : MOV  0x59, R6
0104	 (01 00) 	 : AJMP  0x0
0106	 (fb) 		 : MOV R3, A
0107	 (ac 53) 	 : MOV R4,  0x53
0109	 (ad 54) 	 : MOV R5,  0x54
010b	 (ae 55) 	 : MOV R6,  0x55
010d	 (8c 25) 	 : MOV  0x25, R4
010f	 (8d 26) 	 : MOV  0x26, R5
0111	 (8e 27) 	 : MOV  0x27, R6
0113	 (ec) 		 : MOV A, R4
0114	 (c3) 		 : CLR C
0115	 (13) 		 : RRC A
0116	 (f5 25) 	 : MOV  0x25, A
0118	 (30 26 02)  : JNB  0x26, 0x11c
011b	 (d2 22) 	 : SETB  0x22
011d	 (ed) 		 : MOV A, R5
011e	 (c3) 		 : CLR C
011f	 (13) 		 : RRC A
0120	 (f5 26) 	 : MOV  0x26, A
0122	 (30 27 02)  : JNB  0x27, 0x126
0125	 (d2 21) 	 : SETB  0x21
0127	 (ee) 		 : MOV A, R6
0128	 (c3) 		 : CLR C
0129	 (13) 		 : RRC A
012a	 (f5 27) 	 : MOV  0x27, A
012c	 (ac 25) 	 : MOV R4,  0x25
012e	 (ad 26) 	 : MOV R5,  0x26
0130	 (ae 27) 	 : MOV R6,  0x27
0132	 (db df) 	 : DJNZ R3,  0x213
0134	 (8c 53) 	 : MOV  0x53, R4
0136	 (8d 54) 	 : MOV  0x54, R5
0138	 (8e 55) 	 : MOV  0x55, R6
013a	 (22) 		 : RET
013b	 (aa 59) 	 : MOV R2,  0x59
013d	 (a9 58) 	 : MOV R1,  0x58
013f	 (a8 57) 	 : MOV R0,  0x57
0141	 (ad 55) 	 : MOV R5,  0x55
0143	 (ac 54) 	 : MOV R4,  0x54
0145	 (ab 53) 	 : MOV R3,  0x53
0147	 (7e 00) 	 : MOV R6,  #0x0
0149	 (e8) 		 : MOV A, R0
014a	 (2b) 		 : ADD A, R3
014b	 (50 01) 	 : JNC  0x14e
014d	 (09) 		 : INC R1
014e	 (f5 25) 	 : MOV  0x25, A
0150	 (e9) 		 : MOV A, R1
0151	 (2c) 		 : ADD A, R4
0152	 (50 01) 	 : JNC  0x155
0154	 (0a) 		 : INC R2
0155	 (f5 26) 	 : MOV  0x26, A
0157	 (ea) 		 : MOV A, R2
0158	 (2d) 		 : ADD A, R5
0159	 (50 01) 	 : JNC  0x15c
015b	 (0e) 		 : INC R6
015c	 (f5 27) 	 : MOV  0x27, A
015e	 (22) 		 : RET
