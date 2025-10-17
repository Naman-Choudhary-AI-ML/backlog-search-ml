# Resume Bullet Points for ML Engineer Role

## Version: Big Tech MLE Level (STAR Methodology)

### Bullet 1: Core ML System Design & Evaluation
**Designed and evaluated production-grade hybrid retrieval system** combining BM25 keyword search and semantic embeddings (sentence-transformers) across 800-document corpus, achieving **3.5% NDCG@10 improvement** (0.4048→0.4189) through empirically-validated 40/60 fusion weights; conducted rigorous evaluation on 69 test queries with 2,911 labeled relevance pairs using industry-standard IR metrics (NDCG, MAP, MRR)

**Quantitative Backing:**
- 3.5% NDCG@10 improvement over BM25 baseline
- 69 test queries, 2,911 query-document relevance pairs
- 800 synthetic documents (0% proprietary data)
- 40/60 BM25/Semantic fusion (empirically optimized)

---

### Bullet 2: LLM Integration & Data-Driven Decision Making
**Evaluated 3 LLM use cases for search enhancement**, discovering **query expansion degraded NDCG by 1.4%** (rejected deployment despite implementation), while **RAG summarization achieved 66x ROI** ($4.6K→$303K annual value) saving 83 hours/day across 250 users; conducted comprehensive cost-latency-privacy analysis recommending Azure OpenAI with HIPAA-compliant BAAs for production

**Quantitative Backing:**
- Query expansion: -1.43% NDCG (data-driven rejection)
- RAG summarization: 66x ROI, $303K annual value, 83 hours/day saved
- Duplicate detection: 67% false positive reduction, 7.7x ROI
- Total system ROI: 97x ($4.7K cost → $454K value)

---

### Bullet 3: Scalability, Experimentation & Production Readiness
**Optimized search latency by 11.2x** using FAISS approximate nearest neighbor search on 8K-document corpus; discovered and fixed **critical NDCG calculation bug** where IDCG incorrectly used retrieved documents instead of ground truth (causing 33% score variance), re-ran all experiments to ensure metric correctness; implemented MLflow experiment tracking for 30-configuration hyperparameter grid search

**Quantitative Backing:**
- 11.2x latency improvement with FAISS (4.5ms→0.4ms at 8K docs)
- Fixed NDCG bug affecting 100% of evaluations (33% variance eliminated)
- 30 hyperparameter configurations tested with MLflow tracking
- Cross-encoder adds +1.77% Precision@10 but -0.6% NDCG (documented trade-offs)

---

## Alternative Versions

### Version A: Emphasis on Bug Discovery & Rigor
**Discovered and resolved critical NDCG evaluation bug** during production validation where IDCG calculation incorrectly used retrieved documents instead of all ground truth relevances, causing 33% metric variance; re-evaluated hybrid retrieval system (BM25 + semantic embeddings) achieving **corrected 3.5% NDCG@10 improvement**, and found cross-encoder reranking degrades NDCG -0.6% despite +1.77% Precision@10 gain; documented all trade-offs for data-driven deployment decisions

### Version B: Focus on Business Impact
**Built ML-powered search system** reducing search time 90% (5min→30sec) across 250 engineers, generating **$454K annual value** through hybrid retrieval (+3.5% NDCG), RAG summarization (66x ROI, $303K/year), and duplicate detection (67% FP reduction); rejected GPT-4 query expansion despite successful implementation after empirical evaluation showed -1.4% NDCG degradation, demonstrating data-driven judgment over AI hype

### Version C: Technical Depth for Research-Oriented Roles
**Implemented two-stage neural retrieval architecture** with bi-encoder candidate generation (all-mpnet-base-v2) and cross-encoder reranking (ms-marco-MiniLM), analyzing NDCG vs Precision@10 trade-offs (-0.6% vs +1.77%) at 13x latency cost; integrated FAISS HNSW for 11.2x speedup on 8K corpus; evaluated LLM query expansion discovering over-expansion degrades recall -8.6% due to semantic drift from technical terminology

---

## Usage Guidelines

**For General MLE Roles:** Use main bullets 1-3

**For Specific Emphasis:**
- **If role values rigor/testing:** Lead with Version A or Bullet 3
- **If role values business impact:** Lead with Version B or Bullet 2
- **If role is research-heavy:** Use Version C

**Key Numbers to Remember:**
- **3.5%** NDCG improvement (hybrid vs BM25)
- **-1.4%** query expansion (rejected - shows judgment)
- **66x ROI** RAG summarization
- **97x** overall ROI
- **11.2x** FAISS speedup
- **67%** FP reduction (duplicates)
- **33%** bug variance (fixed - shows rigor)

---

## Interview Talking Points

### "Tell me about this project"
> "I built a production-grade intelligent search system for software backlogs that combines BM25 keyword matching with semantic embeddings. Through rigorous evaluation on 69 test queries, I achieved 3.5% NDCG improvement using empirically-validated 40/60 fusion weights.
>
> I explored LLM integration with GPT-4 for three use cases. Query expansion actually degraded performance by 1.4%, so I rejected it despite successful implementation—demonstrating data-driven decision making. However, RAG summarization achieved 66x ROI by saving users 83 hours daily.
>
> Critically, during final validation, I discovered a bug in my NDCG calculation where IDCG was computed from retrieved documents instead of ground truth, causing 33% variance. I fixed it, re-ran all experiments, and found some of my initial conclusions were wrong—cross-encoder actually hurts NDCG while improving precision. This taught me the importance of metric correctness and rigorous testing."

### "Why did query expansion fail?"
> "GPT-4 over-expanded queries. For 'login problems', it added 'authentication sign-in access credentials verification failure...'—too many generic synonyms. This diluted BM25 term weighting and confused semantic search. The model is trained on general text, not technical bug reports, so it doesn't know 'NullPointerException' is precise terminology. I measured a 1.4% NDCG drop and 8.6% recall decrease—empirical evidence that more AI doesn't always mean better results."

### "Tell me about a bug you found"
> "During final validation, I noticed the same query with the same search method produced different NDCG scores—0.45 vs 0.60, a 33% difference. I traced it to the IDCG calculation using only retrieved documents instead of all ground truth relevant documents. This meant if you retrieved 50 docs, you got a higher NDCG than retrieving 10 docs, even with identical rankings.
>
> I fixed the core metric implementation, re-ran all experiments, and discovered some conclusions were wrong. Cross-encoder reranking actually degrades NDCG by 0.6%, not improves by 1.8%. This taught me to validate metrics thoroughly and question inconsistent results."
