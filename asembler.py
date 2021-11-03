# prevodi asemblerski jezik u binarni

import sys, os

INST = {
    # bezadresne
    'HALT':     '10000000 00000000',
    'RTS':      '10000001 00000000',
    'RTI':      '10000010 00000000',
    'STBR0':    '10000100 00000000',
    'STXR0':    '10000101 00000000',
    'STBR1':    '10000110 00000000',
    'STXR1':    '10000111 00000000',
    'STRCPY':   '10001000 00000000',
    'STAR':     '10001001 00000000',

    # uslovni skok
    'JNEQ':     '11000001 00000000 [INST2]',
    'JLSSU':    '11000010 00000000 [INST2]',
    'JLSS':     '11000100 00000000 [INST2]',

    # bezuslovni skok
    'JMP':      '01000000 00000000 [INST2]',

    # adresne instrukcije
    'LD':       '00110000 [ADDR] [INST]',
    'ST':       '00110001 [ADDR] [INST]',
    'AND':      '00110010 [ADDR] [INST]',
    'ADD':      '00110011 [ADDR] [INST]',
    'CMP':      '00110100 [ADDR] [INST]',
    'JSR':      '00110101 [ADDR] [INST]',
    'CLR':      '00110110 [ADDR] [INST]',
}

BIN2HEX = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}

def toBin(a, pom = 16):
    bin_a = bin(a)[2:]
    while (len(bin_a)) < pom:
        bin_a = '0'+bin_a
    return bin_a

def decodeAddr(INST_ADDR):
    # provera za immmed
    if INST_ADDR.startswith('#'):
        data = int('0'+INST_ADDR[1:].replace('0x', '').replace('0X', ''), 16)
        return ('00000000', toBin(data))

    # provera za memdir
    elif (INST_ADDR.startswith("(") and INST_ADDR[1] in '0123456789' ):
        data = int('0'+INST_ADDR[1:].replace('0x', '').replace('0X', '').replace(')',''), 16)
        return ('00010000', toBin(data))

    # provera za regdir
    elif (INST_ADDR.startswith('DR') ):
        return ('00100000', '')
    
    # provera za regind
    elif (INST_ADDR.startswith('(AR)') ):
        return ('00110000', '')

    # provera za brpom
    elif (INST_ADDR.startswith("(BR") ):
        data = int('0'+INST_ADDR[5:].replace('0x', '').replace('0X', ''), 16)
        return ('0100000'+INST_ADDR[3], toBin(data,8)+'00000000')

    # provera za xrpom
    elif (INST_ADDR.startswith("(XR") ):
        data = int('0'+INST_ADDR[5:].replace('0x', '').replace('0X', ''), 16)
        return ('0101000'+INST_ADDR[3], toBin(data,8)+'00000000')

    # provera za bxpom
    elif ('+' in INST_ADDR):
        data = int('0'+INST_ADDR.split(')')[1].replace('0x', '').replace('0X', ''), 16)
        return ('0110000'+INST_ADDR[0], toBin(data, 8)+'00000000')
    
def assemble(filename):
    # ucitaj fajl
    try:
        f = open(filename, 'r')
        data = f.read()
        f.close()
    except:
        print("* Nepostojan fajl *")
        sys.exit(0)

    # formatiraj fajl
    data = data.replace('\r', '')
    while "  " in data:
        data = data.replace("  ", ' ')

    instr = [i.strip() for i in data.split('\n') if i.strip() and not i.strip().startswith("//") ]

    # dekoduj instrukcije
    binary = []
    # otvori fajl za pisanje i zapisi pocetne nule
    f = open('LOGISIM_ROM_MEM', 'w')
    csv = open("INSTRUCTION_SET.csv", 'w')
    csv.write("Instrukcija,31..24,23..16,15..8,7..0\n")
    f.write("v2.0 raw\n4096*0 ")
    for inst in instr:
        # dohvati naziv instrukcije
        CODE = inst.split(' ')[0].upper()
        if CODE not in INST:
            print(f"*Greska pri dekodovanju instrukcije: {CODE}")
            sys.exit(0)

        # dohvati binarnu reprezentaciju instrukcije
        BIN = INST[CODE]

        # ubaci adresu skoka kod instrukcija skokova
        if ('[INST2]' in BIN):
            addr = int(inst.split(' ')[1].replace('0x', '').replace('0X', ''), 16)
            bin_addr = bin(addr)[2:]
            while len(bin_addr) < 16:
                bin_addr = '0'+bin_addr
            BIN = BIN.replace('[INST2]', bin_addr)

        # proveri nacin adresiranja kod adresnih instrukcija
        if ('[ADDR]' in BIN):
            INST_ADDR = inst.split(' ', 1)[1]
            data = decodeAddr(INST_ADDR)
            BIN = BIN.replace('[ADDR]', data[0]).replace('[INST]', data[1])

        # formatiranje bin coda
        BIN = BIN.replace(' ', '')
        HEX = hex(int(BIN, 2))[2:]
        while (len(HEX) < len(BIN)/4):
            HEX = '0' + HEX

        print (f"-> Dekodovao instrukciju: {inst} ({BIN}/{HEX})")
        for i in range(len(HEX)):
            f.write(HEX[i])
            if ((i+1)%4==0): f.write(" ")

        csv.write(f"{inst},")
        for i in range(0,len(BIN),8):
            csv.write(""+BIN[i:i+8]+"b,")
        if (len(BIN) < 32): csv.write(",,")
        for i in range(len(HEX)):
            csv.write(HEX[i])
            if ((i+1)%4==0): csv.write("h,")
        csv.write("\n")

    f.close()

if __name__ == "__main__":
    print ("*** Asembler za procesor zadatka 41 ***")
    print("\n* Specifikacije procesora *\n- Jednoadresne instrukcije\n- Kolicina memorije: 128KB\n- Program krece od adrese: 1000h\n- Output ROM: LOGISIM_ROM_MEM")
    if (len(sys.argv) < 2):
        print("* GRESKA: Prvi argument mora biti fajl asemblerskog koda *")
        sys.exit(0)

    print("\n* Asemblerski log *")
    assemble(sys.argv[1])