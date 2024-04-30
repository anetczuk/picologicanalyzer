#
#
#

# ================================================

# value for programming
DEVICE     = t85

# value for compiling
MCUDEVICE  = attiny85

# cloc configured by fuses
CLOCK      = 1000000
PROGRAMMER = usbasp
PROG_PORT  = usb

# for ATTiny85 see:
# http://eleccelerator.com/fusecalc/fusecalc.php?chip=attiny85
# http://www.engbedded.com/fusecalc/

FUSES      = -U lfuse:w:0x62:m -U hfuse:w:0xdf:m

# ================================================

INCLUDEDIR = ../include
SRCDIR     = ../src
BUILDDIR   = bin

# Tune the lines below only if you know what you are doing:
AVRDUDE = avrdude -c $(PROGRAMMER) -p $(DEVICE) -P $(PROG_PORT) -B10

COMPILE = avr-gcc -I $(INCLUDEDIR) -Wall -Os -DF_CPU=$(CLOCK) -mmcu=$(MCUDEVICE)

# ================================================

## $(BUILDDIR) in PHONY causes project to rebuild every time
.PHONY: compile $(BUILDDIR)

## first, default rule
compile: $(BUILDDIR)/main.hex

clean:
	rm -f $(BUILDDIR)/main.hex $(BUILDDIR)/main.elf $(OBJECTS)

fuse:
	sudo $(AVRDUDE) $(FUSES)

flash:	compile
	sudo $(AVRDUDE) -U flash:w:$(BUILDDIR)/main.hex:i
	@echo Flashed at: $(shell date)

# Xcode uses the Makefile targets "", "clean" and "install"
deploy: flash fuse

# Targets for code debugging and analysis:
disasm:	$(BUILDDIR)/main.elf
	avr-objdump -d $(BUILDDIR)/main.elf


# ==================== objects rules ====================


## prevents from searching default implicit rule 'Makefile'
Makefile:
	@## do nothing


$(BUILDDIR): Makefile
	@echo Creating dir: \'$(BUILDDIR)\'
	@rm -rf $(BUILDDIR)
	@mkdir -p $(BUILDDIR)


## empty definition makes Makefile faster
%.c:
	@## do nothing

$(BUILDDIR)/%.o: $(SRCDIR)/%.c
	@echo Assembling: \'$<\' to \'$@\'
	@mkdir -p $(BUILDDIR)
	$(COMPILE) -c $< -o $@


OBJECTS = $(BUILDDIR)/main.o

$(BUILDDIR)/main.elf: $(OBJECTS)
	@echo Building: \'$@\'
	@$(COMPILE) -o $(BUILDDIR)/main.elf $(OBJECTS)

$(BUILDDIR)/main.hex: $(BUILDDIR)/main.elf
	@echo Building: \'$@\'
	@rm -f $(BUILDDIR)/main.hex
	@avr-objcopy -j .text -j .data -O ihex $(BUILDDIR)/main.elf $(BUILDDIR)/main.hex
	@echo
	@avr-size --format=avr --mcu=$(MCUDEVICE) $(BUILDDIR)/main.elf

# If you have an EEPROM section, you must also create a hex file for the
# EEPROM and add it to the "flash" target.
