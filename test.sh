for i in {1..9}; do
    files=$(ls json/${i}_*.json)
    python docClassifier.py $files
done