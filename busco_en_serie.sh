INPUT_DIR="/home/lconreur/work/busco"
OUTPUT_DIR="/home/lconreur/work/busco/output"
LINEAGE="polyporales_odb12"
THREADS=8
mkdir -p "$OUTPUT_DIR"
for FILE in "$INPUT_DIR"/*.fasta; do
    BASENAME=$(basename "$FILE" .fasta)
    echo " Analyse de $BASENAME..."
    busco -i "$FILE" \
          -l "$LINEAGE" \
          -o "$BASENAME" \
          -m genome \
          --out_path "$OUTPUT_DIR" \
          --cpu "$THREADS"
done