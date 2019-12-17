MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
BASE_DIR := $(MAKEFILE_DIR)/..
KNP_FILES_TOP_DIR := $(BASE_DIR)/in
PYTHON := python3

OUT_FILES_TOP_DIR := $(BASE_DIR)/out

GZIP_EXT := gz
KNP_FILES := $(shell find -L $(KNP_FILES_TOP_DIR) -type f -name '*.knp.$(GZIP_EXT)')
OUT_FILES := $(patsubst $(KNP_FILES_TOP_DIR)/%.knp.$(GZIP_EXT), $(OUT_FILES_TOP_DIR)/%.tsv.$(GZIP_EXT), $(KNP_FILES))

NICE := nice -19

ifdef COMPOUND
EXTRACT_TRIPLES_FROM_KNP_OPTIONS := --compound
else
EXTRACT_TRIPLES_FROM_KNP_OPTIONS :=
endif

all: $(OUT_FILES)

$(OUT_FILES): $(OUT_FILES_TOP_DIR)/%.tsv.$(GZIP_EXT): $(KNP_FILES_TOP_DIR)/%.knp.$(GZIP_EXT)
	mkdir -p $(dir $@) && \
	$(NICE) gzip -dc $< | $(NICE) $(PYTHON) $(MAKEFILE_DIR)/extract-triples-from-knp.py $(EXTRACT_TRIPLES_FROM_KNP_OPTIONS) | $(NICE) gzip > $@
