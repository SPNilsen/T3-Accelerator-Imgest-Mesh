
# Generate HTML
pandoc docs/test-pandoc.md \
  --metadata-file=meta/header.yaml \
  --metadata date="$(date '+%B %d, %Y')" \
  --standalone \
  --toc --toc-depth=2 \
  --number-sections \
  --section-divs \
  --include-in-header=assets/html/header.html \
  --css=assets/css/styles.css \
  --filter pandoc-crossref \
  --mathjax \
  --resource-path=docs \
  -o out/output.html && open out/output.html

# Generate PDF
pandoc docs/test-pandoc.md \
  --metadata-file=meta/header.yaml \
  --metadata date="$(date '+%B %d, %Y')" \
  --pdf-engine=xelatex \
  --toc --toc-depth=2 \
  --number-sections \
  --filter pandoc-crossref \
  --resource-path=docs \
  --include-in-header=assets/latex/header.tex \
  -o out/output.pdf && open out/output.pdf
