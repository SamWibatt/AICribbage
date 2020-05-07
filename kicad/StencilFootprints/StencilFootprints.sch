EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "SAMD21 and SAMD51 footprints"
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCU_Microchip_SAMD:ATSAMD21G18A-AUT U1
U 1 1 5EA654AE
P 2250 3000
F 0 "U1" H 2250 1011 50  0000 C CNN
F 1 "ATSAMD21G18A-AUT" H 2250 920 50  0000 C CNN
F 2 "Package_QFP:TQFP-48_7x7mm_P0.5mm" H 1300 1250 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/SAMD21-Family-DataSheet-DS40001882D.pdf" H 2250 4000 50  0001 C CNN
	1    2250 3000
	1    0    0    -1  
$EndComp
$Comp
L MCU_Microchip_SAMD:ATSAMD51J18A-A U2
U 1 1 5EA674A5
P 4500 3050
F 0 "U2" H 4500 1161 50  0000 C CNN
F 1 "ATSAMD51J18A-A" H 4500 1070 50  0000 C CNN
F 2 "Package_QFP:TQFP-64_10x10mm_P0.5mm" H 4500 3050 50  0001 C CIN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/60001507E.pdf" H 4500 3050 50  0001 C CNN
	1    4500 3050
	1    0    0    -1  
$EndComp
$Comp
L ATSAMD21_51_Samwibatt:ATSAMD21E18A-AUT U4
U 1 1 5EA67462
P 8800 2550
F 0 "U4" H 9800 2937 60  0000 C CNN
F 1 "ATSAMD21E18A-AUT" H 9800 2831 60  0000 C CNN
F 2 "Package_QFP:TQFP-32_7x7mm_P0.8mm" H 9800 2790 60  0001 C CNN
F 3 "" H 8800 2550 60  0000 C CNN
	1    8800 2550
	1    0    0    -1  
$EndComp
$Comp
L ATSAMD21_51_Samwibatt:ATSAMD51G19A-MUT U3
U 1 1 5EA681E1
P 5900 2050
F 0 "U3" H 6900 2437 60  0000 C CNN
F 1 "ATSAMD51G19A-MUT" H 6900 2331 60  0000 C CNN
F 2 "Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm" H 6900 2290 60  0001 C CNN
F 3 "" H 5900 2050 60  0000 C CNN
	1    5900 2050
	1    0    0    -1  
$EndComp
$EndSCHEMATC