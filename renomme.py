mkdir -p renomme
find . -type f -name 'scaffold_*' | while read -r file; do
    dir=$(basename "$(dirname "$file")")
    prefix=${dir:0:6}
    base=$(basename "$file")
    newname="${prefix}_${base}"
    cp "$file" "renomme/$newname"
done
