# Microcomputer
This school project successfully implements a fully functional microcomputer with its own assembler supporting up to 19 instructions.

## Computer architecture
The simulated computer consists of 3 main units:
- CPU
- Memory
- Interrupts

![](https://raw.githubusercontent.com/stevomitric/Microcomputer/main/docs/sample1.png)

### CPU
Central processing unit (CPU) is a RISC processor that has 19 instructions total. It is the single most important part of the Microprocessor and it's role is to execute instructions and handle user or system generated interrupts. It consists of 4 blocks which represent phases of instruction execution:
- FETCH
- ADDR
- EXEC
- INTR

**FETCH** phase is responsible for getting the next instruction for execution. Instructions are fetched from Memory unit which is connected to the CPU by an address and a data bus.

**ADDR** phase pulls the required opperands which are specified by the executing instruction. Opperands can be given in instruction itself, by address or by pointers (address to the address).

**EXEC** phase executes the instruction.

**INTR** checks for a pending interrupt. If an interrupt is present, CPU will switch to executing the interrupt by changing it's PC (Program Counter register) accordingly.

![](https://raw.githubusercontent.com/stevomitric/Microcomputer/main/docs/sample2.png)

### Memory

### Bus

### Interrupts

## Assember
