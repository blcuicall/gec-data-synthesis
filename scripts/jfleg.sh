if [ $# -lt 3 ]; then
    print "usage: $0 <devices> <checkpoint_dir> <output_dir>"
    exit 1
fi

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
dir=$script_dir/..

fairseq_dir=$dir/fairseq
checkpoint_dir=$2
data_dir=$dir/data/final_data
m2scorer_dir=$dir/m2scorer
jfleg_dir=$dir/jfleg
output_dir=$3

mkdir -p $output_dir
CUDA_VISIBLE_DEVICES=$1 python $fairseq_dir/interactive.py \
    $data_dir/fairseq_preprocess \
    --path $checkpoint_dir \
    --beam 12 \
    --nbest 12 \
    --remove-bpe \
    --num-workers 28 \
    --source-lang src \
    --target-lang trg \
    < $jfleg_dir/test/jfleg.src \
    > $output_dir/gen.txt

cat $output_dir/gen.txt | grep "^H" | python -c "import sys; x = sys.stdin.readlines(); x = ' '.join([ x[i] for i in range(len(x)) if(i%12 == 0) ]); print(x)" | cut -f3 > $output_dir/gen.out

cat $output_dir/gen.out | sed 's|@@ ||g' | sed '$ d' > $output_dir/gen.hyp

#Calculate M2
#Maxmatch result with spellcheck
python $jfleg_dir/eval/gleu.py -r $jfleg_dir/test/test.ref[0-3] -s $jfleg_dir/test/test.src --hyp $output_dir/gen.hyp > $output_dir/testJFLEGresult

#decode test2014 with spellcheck
CUDA_VISIBLE_DEVICES=$1 python $fairseq_dir/interactive.py \
    $data_dir/fairseq_preprocess \
    --path $checkpoint_dir \
    --beam 12 \
    --nbest 12 \
    --remove-bpe \
    --num-workers 28 \
    --source-lang src \
    --target-lang trg \
    < $jfleg_dir/test/jfleg.spell.src \
    > $output_dir/gen_spell.txt

cat $output_dir/gen_spell.txt | grep "^H" | python -c "import sys; x = sys.stdin.readlines(); x = ' '.join([ x[i] for i in range(len(x)) if(i%12 == 0) ]); print(x)" | cut -f3 > $output_dir/gen_spell.out

cat $output_dir/gen_spell.out | sed 's|@@ ||g' | sed '$ d' > $output_dir/gen_spell.hyp

#Calculate M2
#Maxmatch result with spellcheck
python $jfleg_dir/eval/gleu.py -r $jfleg_dir/test/test.ref[0-3] -s $jfleg_dir/test/test.src --hyp $output_dir/gen_spell.hyp > $output_dir/spellJFLEGresult

