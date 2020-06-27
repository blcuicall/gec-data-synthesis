script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
dir=$script_dir/../../..
process_dir=$dir/data/process_data
orign_dir=$dir/data/orign_data
tmp_dir=$script_dir/../tmp
out_dir=$script_dir/..

lmgec_dir=$dir/lmgec-lite
monolingual_dir=$dir/data/monolingual_data

subword_dir=$dir/subword-nmt
bpe_dir=$dir/data/bpe_data

#准备数据
mkdir $tmp_dir

cp $orign_dir/test2013.src $tmp_dir/dev.src.temp
cp $orign_dir/test2013.trg $tmp_dir/dev.trg.temp
cp $orign_dir/test2014.src $tmp_dir/test.src.temp
cp $process_dir/nucle.notsame.src $tmp_dir/nucle.src.temp
cp $process_dir/nucle.notsame.trg $tmp_dir/nucle.trg.temp
cp $process_dir/lang8.notsame.src $tmp_dir/lang8.src.temp
cp $process_dir/lang8.notsame.trg $tmp_dir/lang8.trg.temp

#将开发集和测试集过拼写检查模型
python $lmgec_dir/lmgec.py $tmp_dir/dev.src.temp -mdl $monolingual_dir/1b.bin -o $tmp_dir/dev.lm.temp -th 0.95
python $lmgec_dir/lmgec.py $tmp_dir/test.src.temp -mdl $monolingual_dir/1b.bin -o $tmp_dir/test.lm.temp -th 0.95

#summary
cat $tmp_dir/lang8.src.temp $tmp_dir/nucle.src.temp > $tmp_dir/train.src.temp
cat $tmp_dir/lang8.trg.temp $tmp_dir/nucle.trg.temp > $tmp_dir/train.trg.temp

#应用bpe
python $subword_dir/subword_nmt/apply_bpe.py \
 -c $bpe_dir/bpe < $tmp_dir/train.src.temp > $tmp_dir/train.src.bpe

python $subword_dir/subword_nmt/apply_bpe.py \
 -c $bpe_dir/bpe < $tmp_dir/train.trg.temp > $tmp_dir/train.trg.bpe

python $subword_dir/subword_nmt/apply_bpe.py \
 -c $bpe_dir/bpe < $tmp_dir/dev.src.temp > $tmp_dir/dev.src.bpe

python $subword_dir/subword_nmt/apply_bpe.py \
 -c $bpe_dir/bpe < $tmp_dir/dev.trg.temp > $tmp_dir/dev.trg.bpe

python $subword_dir/subword_nmt/apply_bpe.py \
 -c $bpe_dir/bpe < $tmp_dir/dev.lm.temp > $tmp_dir/dev.lm.bpe

python $subword_dir/subword_nmt/apply_bpe.py \
 -c $bpe_dir/bpe < $tmp_dir/test.src.temp > $tmp_dir/test.src.bpe

python $subword_dir/subword_nmt/apply_bpe.py \
 -c $bpe_dir/bpe < $tmp_dir/test.lm.temp > $tmp_dir/test.lm.bpe

#拷贝到训练目录
cp $tmp_dir/train.src.bpe $out_dir/train.src
cp $tmp_dir/train.trg.bpe $out_dir/train.trg
cp $tmp_dir/dev.src.bpe $out_dir/dev.src
cp $tmp_dir/dev.lm.bpe $out_dir/dev.src.lm
cp $tmp_dir/dev.trg.bpe $out_dir/dev.trg
cp $orign_dir/test2013.m2 $out_dir/dev.m2
cp $tmp_dir/test.src.bpe $out_dir/test.src
cp $tmp_dir/test.lm.bpe $out_dir/test.src.lm
cp $orign_dir/test2014.m2 $out_dir/test.m2

#删除临时文件
