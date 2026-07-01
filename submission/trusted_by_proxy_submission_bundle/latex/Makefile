PDFS=main.pdf supplement.pdf

.PHONY: all clean

all: $(PDFS)

main.pdf: main.tex refs.bib colm2026_conference.sty colm2026_conference.bst
	latexmk -pdf -interaction=nonstopmode main.tex

supplement.pdf: supplement.tex colm2026_conference.sty
	latexmk -pdf -interaction=nonstopmode supplement.tex

clean:
	latexmk -C main.tex
	latexmk -C supplement.tex
