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
errant_dir=$dir/errant
output_dir=$3

mkdir -p $output_dir

#decode test2014 with no spellcheck
CUDA_VISIBLE_DEVICES=$1 python $fairseq_dir/interactive.py \
    $data_dir/fairseq_preprocess \
    --path $checkpoint_dir \
    --beam 12 \
    --nbest 12 \
    --remove-bpe \
    --num-workers 28 \
    --source-lang src \
    --target-lang trg \
    < $data_dir/test.src \
    > $output_dir/gen.txt

cat $output_dir/gen.txt | grep "^H" | python -c "import sys; x = sys.stdin.readlines(); x = ' '.join([ x[i] for i in range(len(x)) if(i%12 == 0) ]); print(x)" | cut -f3 > $output_dir/gen.out

cat $output_dir/gen.out | sed 's|@@ ||g' | sed '$ d' > $output_dir/gen.hyp

#Calculate M2
#Maxmatch result with no spellcheck
~/python2-env/py2.7env/bin/python2 $m2scorer_dir/m2scorer $output_dir/gen.hyp $data_dir/test.m2 > $output_dir/testM2result

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
    < $data_dir/test.src.lm \
    > $output_dir/gen_spell.txt

cat $output_dir/gen_spell.txt | grep "^H" | python -c "import sys; x = sys.stdin.readlines(); x = ' '.join([ x[i] for i in range(len(x)) if(i%12 == 0) ]); print(x)" | cut -f3 > $output_dir/gen_spell.out

cat $output_dir/gen_spell.out | sed 's|@@ ||g' | sed '$ d' > $output_dir/gen_spell.hyp

#Calculate M2
#Maxmatch result with spellcheck
~/python2-env/py2.7env/bin/python2 $m2scorer_dir/m2scorer $output_dir/gen_spell.hyp $data_dir/test.m2 > $output_dir/spellM2result

