#!/bin/bash

python -m pyserini.eval.trec_eval -q ./files/qrels_10_Queries ./results/Dinit_qld.txt > ./results/Dinit_eval.txt
