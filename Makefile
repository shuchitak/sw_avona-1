# This variable is used for setting the EXECUTABLE name
# and is used for the final binary, as well as any intermediates.
PROJECT_NAME = sw_avona

# BOARD is used by the XMOS RTOS platform .cmake file
BOARD ?= XCORE-AI-EXPLORER
WW ?= amazon
APP_CONF_DEFINES ?=

CMAKE_ARGS ?=
CMAKE_ARGS += -DUSE_WW=$(WW) -DAPP_CONF_DEFINES=$(APP_CONF_DEFINES)

# PLATFORM_USES_TILE_0 through PLATFORM_USES_TILE_3 are
# used by the multitile_build.mk file. If only tile 0 is
# used then none of these need to be specified.
# 1 must be used to enable any other tiles.  If they
# are not used then they do not need to be specified,
# but may be set to 0.
PLATFORM_USES_TILE_0 = 1
PLATFORM_USES_TILE_1 = 1
PLATFORM_USES_TILE_2 = 0
PLATFORM_USES_TILE_3 = 0

# XE_BASE_TILE is used by the multitile_build.mk file.
# It defaults to 0 if not specified.
XE_BASE_TILE = 0

# BUILD_DIR and OUTPUT_DIR are used by the multitile_build.mk file.
# If not specified they default to 'build' and 'bin' respectively.
BUILD_DIR  = build
OUTPUT_DIR = bin

# EXECUTABLE is used by the multitile_build.mk file
# and it must be specified, and set to the file name
# (including relative path) of the ultimate .xe file
# that contains all the merged tile binaries.
EXECUTABLE = $(OUTPUT_DIR)/$(PROJECT_NAME).xe

.PHONY: all clean distclean run

all: $(EXECUTABLE)

# MULTITILE_CLEANUP_CMDS is a variable generated by
# multitile_build.mk and may be included here in clean's
# recipe to perform cleanup of the files generated by
# multitile_build.mk.
clean:
	$(MULTITILE_CLEANUP_CMDS)
	rm -f $(EXECUTABLE)

distclean:
	rm -rf $(BUILD_DIR)
	rm -rf $(OUTPUT_DIR)

run: $(EXECUTABLE)
	xrun --xscope-file scope $(EXECUTABLE)

flash: $(EXECUTABLE)
	cd filesystem_support && ./flash_image.sh

# This multitile build support file c the
# recipe for EXECUTABLE
include $(XCORE_SDK_PATH)/tools/cmake_utils/multitile_build.mk
