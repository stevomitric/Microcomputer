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
Memory used in this project is of 128 KB size, with 2 B as smallest adresabile unit. Size of adress and data bus is 16 bit.

To simulate real-world memory responses, a random delay is added to each memory request. This delay can be anywhere from 0-15 ticks.

![](https://raw.githubusercontent.com/stevomitric/Microcomputer/main/docs/sample3.png)

### Bus
Bus is a component responsible for connecting every module and allowing them to communicate. CPU and Memory are connected via 3 bus lines:
- Address bus (ABUS)
- Data bus (DBUS)
- Control bus (CBUS)

Communication between these two modules looks like this (reading data):
1. CPU puts an address from which its requests data on ABUS
2. CPU activates RD signal on CBUS
3. Memory fetches the requested data and puts it on DBUS
4. Memory activates FC signal on CBUS
5. CPU takes the data from DBUS and disables RD signal

### Interrupts
Interrupt mechanizam allows for preemptive workflow. After each instruction is executed, CPU checks if interrupt has happend and if so, jumps to specific interrupt function. If jump occured, CPU also saves its context first, which consists of AX (Acumulator), PC (Program counter) and PSW (Program status word) registers, on stack.

To simulate interrupts happening from end-users, 8 buttons are added to interrupt-UI. All interrupts are masked and higher number interrupt has higher priority. 

## Assember
