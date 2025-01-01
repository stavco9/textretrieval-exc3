import os
from pyserini.index.lucene import IndexReader
from pyserini.analysis import Analyzer, get_lucene_analyzer
from pyserini.search import get_topics_with_reader, LuceneSearcher

# Load TSV-format topics
topic_file_path = "./files/10_ROBUST_Queries.txt"
topics=get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader',topic_file_path)
#fix query ids
queries = {}
for topic_id, topic in topics.items():
    fixed_topic_id = str(topic_id)
    if len(fixed_topic_id) == 2:
        fixed_topic_id = '0'+str(topic_id)
    queries[fixed_topic_id] = topic['title']
assert len(queries) == 10, 'missing queries'

index_path = './RobustPyserini'
searcher = LuceneSearcher(index_path)
# specify custom analyzer for the query processing step to match the way the index was built
analyzer = get_lucene_analyzer(stemmer='krovetz', stopwords=False) # Ensure no stopwords are removed from the query
searcher.set_analyzer(analyzer)
# Optionally, configure BM25 parameters (can be adjusted as needed)
searcher.set_qld(mu=1000)

results = {} # To store results for each query
for topic_id, topic in queries.items():
    hits = searcher.search(topic,k=1000) # k=1000 is the number of retrieved documents
    # Store results in TREC format for each topic
    results[topic_id] = [(hit.docid, i+1, hit.score) for i, hit in enumerate(hits)]

# Now you can save the results to a file in the TREC format:
output_file = f'./results/Dinit_qld.txt'
if not os.path.exists('./results'):
    os.makedirs('./results')
sorted_results = dict(sorted(results.items()))
with open(output_file, 'w') as f:
    for topic_id, hits in sorted_results.items():
        for rank, (docid, _, score) in enumerate(hits, start=1):
            f.write(f"{topic_id} Q0 {docid} {rank} {score:.4f} pyserini\n")