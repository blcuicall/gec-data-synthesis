virtualenv -p /usr/bin/python3.6 ~/python3-env/py3.6env
cat 'source ~/python3-env/py3.6env/bin/activate' >> ~/.bashrc
source ~/.bashrc

#m2scorer(need python2.7)
git clone https://github.com/nusnlp/m2scorer.git
cp modified_code/m2scorer.py m2scorer/scripts/
cp modified_code/levenshtein.py m2scorer/scripts/

#subword-nmt
git clone https://github.com/rsennrich/subword-nmt.git

#lmgec-lite (lm spellcheck)
git clone https://github.com/chrisjbryant/lmgec-lite.git
git cline https://github.com/kpu/kenlm.git
mkdir kenlm/build
cd kenlm/build
cmake ..
make -j 4
pip install https://github.com/kpu/kenlm/archive/master.zip
pip install numpy==1.14.5
pip install -U spacy==1.9.0
python -m spacy download en
pip install -U CyHunspell

cp modified_code/lmgec.py lmgec-lite/

#fairseq (transformer)
git clone https://github.com/pytorch/fairseq.git
pip install torch==1.0.0
pip install torchvision
pip install fairseq

#mlconvgec2018
git clone https://github.com/nusnlp/mlconvgec2018.git
cp modified_code/prepare_data.sh mlconvgec2018/data
