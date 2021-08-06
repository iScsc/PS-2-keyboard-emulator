BLACK        := $(shell tput -Txterm setaf 0)
RED          := $(shell tput -Txterm setaf 1)
GREEN        := $(shell tput -Txterm setaf 2)
YELLOW       := $(shell tput -Txterm setaf 3)
LIGHTPURPLE  := $(shell tput -Txterm setaf 4)
PURPLE       := $(shell tput -Txterm setaf 5)
BLUE         := $(shell tput -Txterm setaf 6)
WHITE        := $(shell tput -Txterm setaf 7)
RESET        := $(shell tput -Txterm sgr0)

##################
## PARAMETERS ####
##################
ARD     = arduino#                          # the arduino executable.
BOARD   = arduino:avr:mega:cpu=atmega2560#  # the full board name, can be browsed easily.
PORT    = /dev/ttyACM0#                     # the device port on the host machine.
SRC_ARD = src/arduino_side/arduino_side.ino## the source for the arduino part.

PY     = python#            # the python executable.
SRC_PY = src/laptop_side.py## the source for the host part.

##################
## Makers ########
##################
# emulate, i.e. device and host.
all: emulate

# emulate.
emulate: device host

# only the device part.
device:
	@echo "$(LIGHTPURPLE)$(ARD) --board $(BOARD) --port $(PORT) --upload $(SRC_ARD)$(RESET)"
	@$(ARD) --board $(BOARD) --port $(PORT) --upload $(SRC_ARD)

# only the host part.
host:
	@echo "$(LIGHTPURPLE)$(PY) $(SRC_PY)$(RESET)"
	@$(PY) $(SRC_PY)
