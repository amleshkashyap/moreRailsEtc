## [Bochs](https://bochs.sourceforge.io/)
  * Intel x86 simulator
    - CPU
      - 386, 486, pentium
      - pentium 6 and ahead
      - x86-64 extensions
      - floating point units
    - Common I/O Devices
      - keyboard, mouse, VGA card/monitor, hard disk
      - PCI, USB, CD-ROM, sound card, network card, floppy disk
      - multiprocessors, parallel and serial ports, 3D video card, game port
    - BIOS, CMOS
    - Virtualization - no

  * Can run on different host platforms - x86, MIPS, Sun, Alpha
    - Due to complete hardware simulation, it's very slow
    - Commercial emulators (vmware) achieves higher speed with virtualization, but can't run on non-x86 (or whatever they were designed for)

  * Basics
    - Bochs interacts with the host OS regularly
    - For user input via keyboard, an event goes to device model for keyboard
    - For disk space in the simulator, a disk image file is present on the host machine
    - When simulator has an application that sends a network packet, Bochs uses host OS network card to send it outside
    - Eg, sending a network packet in FreeBSD has different code than Windows XP - hence, certain features are not supported on all host OS

## [QEMU](https://www.qemu.org/docs/master/system/index.html)
  * Machine and userspace emulator, virtualizer
    - Can emulate hardware without hardware virtualization - speed maybe better than bochs as it uses dynamic translation.
    - Can integrate with KVM/Xen hypervisors to provide emulated hardware, letting the hypervisor manage the CPU.
    - Can provide userspace API virtualization (linux/BSD kernels) - only CPU and syscall emulation
