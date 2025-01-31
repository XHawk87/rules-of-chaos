# Define variables
RULESET_NAME = Chaos
CONFIG_JSON = game.json
FILTERS = filters.py
TESTS = tests.py
J2_DEPS = $(CONFIG_JSON) $(FILTERS) $(TESTS)
J2CLI = j2 $< $(CONFIG_JSON) \
		--filters $(FILTERS) \
		--tests $(TESTS) \
		--import-env= \
		-o $@
SERVER_BIN = freeciv21-server

INCLUDES_DIR = includes
SRC_DIR = src
DEST_DIR = game

# Generate list of destination files from sources
SRC_FILES = $(shell find $(SRC_DIR)/ -type f)
DEST_FILES = $(patsubst $(SRC_DIR)/%, $(DEST_DIR)/%, $(subst .j2,,$(SRC_FILES)))

# Define the target for all files
all: build

build: $(DEST_DIR) $(DEST_FILES)

# Clean out the destination directory for a full rebuild
clean: $(DEST_DIR)
	rm --verbose --recursive --force $(DEST_DIR)

clean-build: clean build

run-local: build
	(cd "$(DEST_DIR)" && $(SERVER_BIN) --read $(realpath ./$(DEST_DIR)/dev.serv) --log server.log)

# Rules to ensure the destination directories exist
$(DEST_DIR):
	mkdir --verbose --parents $(DEST_DIR)

# Pattern rules for processing .j2 files
SCRIPTS = $(shell find $(INCLUDES_DIR)/scripts/ -mindepth 1 -type f)
$(DEST_DIR)/$(RULESET_NAME)/script.lua: $(SRC_DIR)/$(RULESET_NAME)/script.lua.j2 $(DEST_DIR) $(J2_DEPS) $(SCRIPTS)
	@mkdir --verbose --parents $(dir $@)
	$(J2CLI)

$(DEST_DIR)/%: $(SRC_DIR)/%.j2 $(DEST_DIR) $(J2_DEPS)
	@mkdir --verbose --parents $(dir $@)
	$(J2CLI)

# Rule for static files
$(DEST_DIR)/%:: $(SRC_DIR)/% $(DEST_DIR)
	@mkdir --verbose --parents $(dir $@)
	cp --verbose --force $< $@

# Mark targets that are not files
.PHONY: all build clean clean-build run-local
