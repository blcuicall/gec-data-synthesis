if [ $# -lt 6 ]; then
    print "usage: $0 <devices> <checkpoint_dir> <restore_dir> <average_dir> <seed> <update_dreq>"
    exit 1
fi

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
dir=$script_dir/..

fairseq_dir=$dir/fairseq
checkpoint_dir=$2
average_num=$4
data_dir=$dir/data/final_data
m2scorer_dir=$dir/m2scorer
errant_dir=$dir/errant

#train
mkdir -p $checkpoint_dir
cp $script_dir/transformer.sh $checkpoint_dir

CUDA_VISIBLE_DEVICES=$1 python $fairseq_dir/train.py $data_dir/fairseq_preprocess \
 --arch 'transformer' --optimizer 'adam' --adam-betas '(0.9, 0.98)' --update-freq $6 \
 --lr '5e-4' --min-lr '1e-9' --warmup-init-lr '1e-7' --dropout 0.3 --max-tokens 4000 \
 --encoder-ffn-embed-dim 2048 --decoder-ffn-embed-dim 2048 --seed $5 \
 --lr-scheduler inverse_sqrt --warmup-updates 4000 --share-decoder-input-output-embed \
 --save-dir $checkpoint_dir --weight-decay 0.0001 --max-update 30000 \
 --criterion gec_label_smoothed_cross_entropy --label-smoothing 0.1 \
 --source-lang src --target-lang trg --task gec --factor 1.2 \
 --restore-file $3 --reset-optimizer --reset-lr-scheduler \
 2>&1 | tee -a $checkpoint_dir/training_log.txt

#average_checkpoint
average_dir=$checkpoint_dir/average_best$average_num
mkdir $average_dir

python $script_dir/get_top_best.py $checkpoint_dir $average_num training_log.txt 'sorted_'$average_num'.txt'

var=$(cat $checkpoint_dir'/sorted_'$average_num'.txt')
python $fairseq_dir/scripts/average_checkpoints.py \
 --inputs $var \
 --output $average_dir/average.pt
