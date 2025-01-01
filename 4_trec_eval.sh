#!/bin/bash

python -m pyserini.eval.trec_eval -q ./files/qrels_10_Queries ./files/Best_Expansion_qld.txt > ./results/Best_Expansion_eval.txt
