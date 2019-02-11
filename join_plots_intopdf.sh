convert -quality 85 `find -maxdepth 1 -type f -name '*.png' -or -name '*.jpg' | sort -V` output.pdf
