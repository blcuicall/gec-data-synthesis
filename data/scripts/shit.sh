#!/bin/bash

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
dir=$script_dir/../..
mlconvgec2018_dir=$dir/mlconvgec2018
process_dir=$dir/data/process_data

monolingual_dir=$dir/data/monolingual_data
kenlm_dir=$dir/kenlm

traindata_dir=$dir/data/final_data

pretraindata_dir=$dir/data/pretrain_data

fairseq_dir=$dir/fairseq

#mkdir $process_dir
##sh $mlconvgec2018_dir/data/prepare_data.sh
#cp $mlconvgec2018_dir/data/lang-8/* $process_dir
#cp $mlconvgec2018_dir/data/nucle-train/nucle-train.tok.* $process_dir
#cp $mlconvgec2018_dir/data/nucle-dev/nucle-dev.tok.* $process_dir

#利用mlconvgec2018脚本清洗分开的数据，去除过长或者过短的数据
#$mlconvgec2018_dir/data/scripts/moses_scripts/clean-corpus-n.perl $process_dir/lang-8.tok src trg $process_dir/lang-8.temp 2 80
#$mlconvgec2018_dir/data/scripts/moses_scripts/clean-corpus-n.perl $process_dir/nucle-train.tok src trg $process_dir/nucle_train 2 80
#$mlconvgec2018_dir/data/scripts/moses_scripts/clean-corpus-n.perl $process_dir/nucle-dev.tok src trg $process_dir/nucle_dev 2 80
#cat $process_dir/nucle_*.src > $process_dir/nucle.temp.src
#cat $process_dir/nucle_*.trg > $process_dir/nucle.temp.trg

#preprocess train data
#python $script_dir/preprocess_traindata.py $process_dir/lang-8.temp.src $process_dir/lang-8.temp.trg $process_dir/ lang8 False
#python $script_dir/preprocess_traindata.py $process_dir/nucle.temp.src $process_dir/nucle.temp.trg $process_dir/ nucle False

#把src与trg一样的和不一样的区分开来
#python $script_dir/split_files.py $process_dir/nucle.src.p $process_dir/nucle.trg.p $process_dir/nucle
#python $script_dir/split_files.py $process_dir/lang8.src.p $process_dir/lang8.trg.p $process_dir/lang8

#删除中间文本
#rm $process_dir/nucle-*
#rm $process_dir/nucle_*
#rm $process_dir/lang-8.tok.*
#rm $process_dir/*.temp.*
#rm $process_dir/*.q
#rm $process_dir/*.p

#summary
#python $script_dir/summary_files.py --i $process_dir --name src --o $process_dir/all.sr
#python $script_dir/summary_files.py --i $process_dir --name trg --o $process_dir/all.tr
#python $script_dir/summary_files.py --i $process_dir --name same --o $process_dir/all.sa

#训练bpe词表
subword_dir=$dir/subword-nmt
bpe_dir=$dir/data/bpe_data
num=50000

#mkdir $bpe_dir
#python $subword_dir/subword_nmt/learn_joint_bpe_and_vocab.py \
# --input $process_dir/all.sr $process_dir/all.tr $process_dir/all.sa \
# -s $num \
# -o $bpe_dir/bpe \
# --write-vocabulary $bpe_dir/vocab.src $bpe_dir/vocab.trg $bpe_dir/vocab.same

#train language model for lmgec-lite spelcheck
#wget http://www.statmt.org/lm-benchmark/1-billion-word-language-modeling-benchmark-r13output.tar.gz -O $monolingual_dir/
#tar -zxvf $monolingual_dir/1-billion-word-language-modeling-benchmark-r13output.tar.gz
#cat $monolingual_dir/1-billion-word-language-modeling-benchmark-r13output/training-monolingual.tokenized.shuffled/* > $monolingual_dir/1b.train.txt
#cat $monolingual_dir/1-billion-word-language-modeling-benchmark-r13output/heldout-monolingual.tokenized.shuffled/* > $monolingual_dir/1b.dev.txt
#$kenlm_dir/build/bin/lmplz -o 5 -S 50% -T $monolingual_dir/ < $monolingual_dir/1b.train.txt > $monolingual_dir/1b.arpa
#$knelm_dir/build/bin/build_binary $monolingual_dir/1b.arpa $monolingual_dir/1b.bin
#rm $monolingual_dir/1b.arpa
#cp $monolingual_dir/1b.train.txt $monolingual_dir/1b.train.temp
#python $script_dir/preprocess_traindata.py $monolingual_dir/1b.train.txt $monolingual_dir/1b.train.temp $process_dir/ wiki False
#python ../scripts/clean_corpus_length.py --i wiki.trg.p --o wiki.clean --min 2 --max 80
#rm $monolingual_dir/1b.train.temp $process_dir/wiki.src.p $process_dir/*.q

#generate the train data
#bash $traindata_dir/scripts/run.sh

#generate the pretrain data
#bash $pretraindata_dir/scripts/run.sh

#generate fairseq preprocess binary data
#if [ -d $traindata_dir/fairseq_preprocess ];then
# rm -r $traindata_dir/fairseq_preprocess
#fi
#python $fairseq_dir/preprocess.py \
#    --srcdict $bpe_dir/share_bpe_vocab \
#    --source-lang src \
#    --target-lang trg \
#    --trainpref $traindata_dir/train \
#    --validpref $traindata_dir/dev \
#    --testpref $traindata_dir/dev \
#    --destdir $traindata_dir/fairseq_preprocess \
#    --workers 28 \
#    --joined-dictionary

#if [ -d $pretraindata_dir/fairseq_preprocess ];then
# rm -r $pretraindata_dir/fairseq_preprocess
#fi
#python $fairseq_dir/preprocess.py \
#    --srcdict $bpe_dir/share_bpe_vocab \
#    --source-lang src \
#    --target-lang trg \
#    --trainpref $pretraindata_dir/train \
#    --validpref $pretraindata_dir/dev \
#    --testpref $pretraindata_dir/dev \
#    --destdir $pretraindata_dir/fairseq_preprocess \
#    --workers 28 \
#    --joined-dictionary

temp_traindata_dir=$dir/data/cls_final_data
#bash $temp_traindata_dir/scripts/run.sh

#if [ -d $temp_traindata_dir/fairseq_preprocess ];then
# rm -r $temp_traindata_dir/fairseq_preprocess
#fi
python $fairseq_dir/preprocess.py \
    --srcdict $bpe_dir/../bak_bpe/share_bpe_vocab \
    --trainpref $temp_traindata_dir/train.trg \
    --validpref $temp_traindata_dir/dev.trg \
    --destdir $temp_traindata_dir/fairseq_preprocess \
    --workers 40 \
    --only-source

