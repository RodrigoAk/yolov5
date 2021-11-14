#!/bin/sh

tmpfile=$(mktemp)

for file in ./coco/labels/val2014_custom/*.txt; do
	cp "$file" "$tmpfile" &&
	sort "$tmpfile" | uniq > "$file"
done

rm "$tmpfile"
