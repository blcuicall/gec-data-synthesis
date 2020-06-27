if [ $# -lt 3 ]; then
    print "usage: $0 <devices> <checkpoint_dir> <update_freq>"
    exit 1
fi

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
dir=$script_dir/..
fairseq_dir=$dir/fairseq
data_dir=$dir/data/pretrain_data
checkpoint_dir=$2

mkdir -p $checkpoint_dir
cp $script_dir/pretrain.sh $checkpoint_dir

CUDA_VISIBLE_DEVICES=$1 python $fairseq_dir/train.py $data_dir/fairseq_preprocess \
 --arch 'transformer' --optimizer 'adam' --adam-betas '(0.9, 0.98)' --update-freq $3 \
 --lr '5e-4' --min-lr '1e-9' --dropout 0.3 --max-tokens 4000 --seed 3 \
 --lr-scheduler inverse_sqrt --warmup-updates 4000 --warmup-init-lr '1e-7' \
 --save-dir $checkpoint_dir --weight-decay 0.0001 --max-epoch 5 --share-decoder-input-output-embed \
 --criterion gec_label_smoothed_cross_entropy --label-smoothing 0.1 \
 --source-lang src --target-lang trg --task gec --factor 1.2 \
 2>&1 | tee -a $checkpoint_dir/training_log.txt

python $fairseq_dir/scripts/average_checkpoints.py \
 --num-epoch-checkpoints 3 \
 --input $checkpoint_dir/ \
 --output $checkpoint_dir/average.pt
