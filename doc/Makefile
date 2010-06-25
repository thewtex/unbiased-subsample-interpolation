# makefile for rendering documents from ReStructured Text

BIB4TXT=bib4txt.py
IMGMATHHACK=formatting/imgmathhack.py
ODTRESPACE=odt-respace
RST2ODT=rst2odt.py
UNOCONV=unoconv

STYLESODT=styles.odt
STYLESODTPATH=formatting/$(STYLESODT)

PAPER=subsample_interpolation

all: $(PAPER).odt

$(PAPER)_w_math.rst: $(PAPER).rst
	$(IMGMATHHACK) $(PAPER).rst $(PAPER)_w_math.rst

# add '-s example_numbered' for numbered references instead of last names
$(PAPER)_w_cite.rst: $(PAPER)_w_math.rst $(PAPER).bib
	PYTHONPATH='./formatting' $(BIB4TXT) -s example_numbered --all -i $(PAPER)_w_math.rst -no $(PAPER)_w_cite.rst $(PAPER).bib

$(PAPER).odt: $(PAPER)_w_cite.rst $(STYLESODTPATH)
	$(RST2ODT) --stylesheet=$(STYLESODTPATH) $(PAPER)_w_cite.rst $(PAPER).odt

$(PAPER)_double_spaced.odt: $(PAPER).odt
	$(ODTRESPACE) $(PAPER).odt $(PAPER)_double_spaced.odt

$(PAPER).doc: $(PAPER)_double_spaced.odt
	$(UNOCONV) -f doc $(PAPER)_double_spaced.odt 
	mv $(PAPER)_double_spaced.doc $(PAPER).doc

clean:
	rm -f $(shell find . -name '*.doc' -or -name '*.odt' -not -name $(STYLESODT) -or -name '*_w_cite.rst' -or -name '*_w_math.rst') mti* imgmath/*
