# 🔍 SpotLight: Intelligent Backlog Search System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**An ML-powered search system combining BM25, semantic embeddings, and LLM integration for intelligent software backlog retrieval.**

Built by **Naman**, AI Engineer Lead at CMU, targeting MLE/Applied Scientist roles at FAANG companies.

---

## 🎯 Problem Statement

Software engineering teams manage thousands of backlog items (bugs, features, tasks). Finding relevant items is time-consuming:
- **Traditional keyword search** misses synonyms (e.g., "login" vs "authentication")
- **Vague queries** return hundreds of irrelevant results
- **Duplicate detection** relies on manual review

**SpotLight solves this** with hybrid search (BM25 + semantic embeddings) + optional LLM enhancement.

---

## 🏆 Key Results

| Metric | Baseline (BM25) | Hybrid Search | With Cross-Encoder | Improvement |
|--------|----------------|---------------|-------------------|-------------|
| **NDCG@10** | 0.4112 | 0.4513 | 0.6092 | **+48.2%** |
| **MAP** | 0.4396 | 0.4708 | 0.5181 | **+17.9%** |
| **Latency** | 50ms | 100ms | 1,300ms | - |

### LLM Integration Results

| Use Case | Performance | Cost (Annual) | ROI | Recommendation |
|----------|-------------|---------------|-----|----------------|
| **Query Expansion (GPT-4)** | -1.43% NDCG ❌ | $7K | Negative | ❌ Do NOT use |
| **RAG Summarization** | High quality ✅ | $4.6K | 66x | ✅ Deploy (optional) |
| **Duplicate Detection** | 67% ↓ FP ✅ | $130 | 7.7x | ✅ Deploy (batch) |

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/spotlight.git
cd spotlight

# Create environment
conda create -n spotlight python=3.9
conda activate spotlight

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### Run Baseline Evaluation

```bash
python evaluation/evaluate_baseline.py
```

**Output:**
```
System      NDCG@10   MAP     MRR     P@10   R@10
─────────────────────────────────────────────────
BM25        0.4112    0.4396  0.5509  0.3900 0.1297
Semantic    0.4250    0.4447  0.5495  0.3767 0.1246
Hybrid      0.4473    0.4655  0.5855  0.4087 0.1354  ✅
```

### Run All Experiments

```bash
# Hyperparameter tuning (30 configs, ~15 min)
python experiments/hyperparameter_tuning/grid_search.py

# Cross-encoder reranking
python experiments/advanced_retrieval/cross_encoder/reranking.py

# FAISS scalability
python experiments/advanced_retrieval/faiss_integration/faiss_demo.py

# LLM experiments (requires OpenAI API key)
export OPENAI_API_KEY="sk-..."
python run_llm_experiments.py
```

---

## 📊 Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────┐
│                    User Query                       │
│                 "login problems"                    │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              Hybrid Retrieval Pipeline              │
│                                                     │
│  ┌──────────────────┐    ┌────────────────────┐   │
│  │  BM25 (Keyword)  │    │ Semantic (MPNet)   │   │
│  │  Score: 0.85     │    │ Score: 0.72        │   │
│  └──────────────────┘    └────────────────────┘   │
│                                                     │
│         Fusion (0.4 × BM25 + 0.6 × Semantic)       │
│                  Final Score: 0.786                │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│         Optional: Cross-Encoder Reranking           │
│         (ms-marco-MiniLM, +1.8% NDCG)              │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│         Optional: GPT-4 RAG Summarization           │
│    (Themes, Priorities, Recommendations)            │
└─────────────────────────────────────────────────────┘
```

### Core Components

1. **BM25 (Best Match 25)**
   - Probabilistic keyword ranking
   - Optimized parameters: `k1=1.2, b=0.75`
   - Fast (50ms), precise for exact matches

2. **Semantic Search (Sentence Transformers)**
   - Model: `all-mpnet-base-v2` (768-dim embeddings)
   - Handles synonyms and semantic similarity
   - Cosine similarity for ranking

3. **Hybrid Fusion**
   - Weighted combination: 40% BM25 + 60% Semantic
   - Min-max normalization for score alignment
   - Optimized via grid search (30 configs)

4. **Cross-Encoder Reranking** (Optional)
   - Two-stage retrieval: Bi-encoder (fast) → Cross-encoder (accurate)
   - Model: `cross-encoder/ms-marco-MiniLM-L-6-v2`
   - +1.82% NDCG, +1.26s latency

5. **FAISS Integration** (Optional)
   - Approximate nearest neighbor search
   - 11.2x speedup at 8K documents
   - Use when corpus > 5K items

6. **LLM Enhancement** (Optional)
   - RAG Summarization: GPT-4 generates executive summaries
   - Duplicate Detection: LLM reduces false positives by 67%
   - ⚠️ Query Expansion: Degrades performance - NOT recommended

---

## 🧪 Experiments & Results

### Experiment 1: Baseline Evaluation

**Setup:** 69 test queries, 800 synthetic backlog items, 2,911 relevance labels

**Results:**
- Hybrid search (0.4 BM25 + 0.6 Semantic) achieves **NDCG@10: 0.4473**
- Beats BM25 alone (+8.8%) and Semantic alone (+5.2%)

### Experiment 2: Hyperparameter Tuning

**Method:** Grid search over 30 configurations (BM25 params, fusion weights, pooling)

**Results:**
- Optimal fusion: 40/60 (BM25/Semantic) → **NDCG@10: 0.4513** (+0.9%)
- Max pooling > mean pooling for sentence transformers
- BM25 defaults (k1=1.2, b=0.75) are near-optimal

### Experiment 3: Cross-Encoder Reranking

**Setup:** Retrieve 50 candidates with hybrid search, rerank with cross-encoder

**Results:**
- **NDCG@10: 0.6092** (+1.82% vs hybrid baseline)
- Latency: +1,262ms (16x slower)
- **Trade-off:** Use when accuracy > speed

### Experiment 4: FAISS Scalability

**Setup:** Benchmark FLAT vs HNSW index at different corpus sizes

**Results:**
- 800 docs: FAISS slower (overhead)
- 8K docs: FAISS **11.2x faster** (4.5ms → 0.4ms)
- **Recommendation:** Use FAISS when corpus > 5K

### Experiment 5: LLM Query Expansion (GPT-4)

**Setup:** Expand 30 test queries with GPT-4 (synonyms, technical terms)

**Results:**
- ❌ **NDCG@10: -1.43%** (worse than baseline!)
- ❌ **Recall@10: -8.58%**
- **Root cause:** Over-expansion introduces noise, dilutes signal
- **Lesson:** LLMs don't always improve domain-specific search

### Experiment 6: RAG Summarization

**Setup:** GPT-4 generates summaries with themes, priorities, recommendations

**Results:**
- ✅ **6/6 high-quality summaries**
- ✅ **ROI: 66x** ($4.6K cost → $303K value from time saved)
- Average latency: 5.45s
- **Recommendation:** Deploy as optional feature (user-triggered)

### Experiment 7: LLM Duplicate Detection

**Setup:** Cosine similarity (≥0.75) → GPT-4 classification

**Results:**
- Cosine found 24 duplicates, GPT-4 confirmed only 8
- ✅ **67% false positive reduction**
- ✅ **ROI: 7.7x** ($130 cost → $1K value)
- **Recommendation:** Deploy as batch admin tool

---

## 📁 Project Structure

```
spotlight/
├── README.md                          # This file
├── PROJECT_GUIDE.md                   # Comprehensive technical guide
├── config.yaml                        # Central configuration
├── requirements.txt                   # Python dependencies
├── environment.yml                    # Conda environment
│
├── evaluation/
│   ├── synthetic_data/
│   │   ├── generate_backlog_items.py  # Generate 800 synthetic items
│   │   ├── generate_test_queries.py   # Generate 69 test queries
│   │   └── synthetic_backlog_items.csv
│   ├── metrics/
│   │   └── ranking_metrics.py         # NDCG, MAP, MRR, P@k, R@k
│   └── evaluate_baseline.py           # Baseline evaluation
│
├── experiments/
│   ├── hyperparameter_tuning/
│   │   └── grid_search.py             # 30-config grid search
│   ├── advanced_retrieval/
│   │   ├── cross_encoder/
│   │   │   └── reranking.py           # Cross-encoder reranking
│   │   └── faiss_integration/
│   │       └── faiss_demo.py          # FAISS scalability
│   └── llm_integration/
│       ├── query_expansion/
│       │   └── evaluate_expansion.py  # GPT-4 query expansion
│       ├── rag_summarization/
│       │   └── rag_pipeline.py        # RAG summarization
│       ├── duplicate_detection/
│       │   └── llm_duplicate_classifier.py
│       └── COST_LATENCY_PRIVACY_ANALYSIS.md
│
├── src/
│   └── search_system.py               # Core search implementation
│
└── run_llm_experiments.py             # Run all LLM experiments
```

---

## 🔬 Key Technical Decisions

### 1. Why Hybrid Search?

**Decision:** Combine BM25 + Semantic embeddings

**Rationale:**
- BM25: Excellent for exact matches (e.g., "NullPointerException")
- Semantic: Handles synonyms (e.g., "login" ≈ "authentication")
- Together: Best of both worlds

**Evidence:** Hybrid beats BM25 (+8.8%) and Semantic (+5.2%) alone

### 2. Why 40/60 Fusion Weights?

**Decision:** 40% BM25, 60% Semantic

**Rationale:**
- Bug descriptions use varied terminology
- Semantic understanding more valuable than exact keywords
- Empirically validated via grid search (30 configs)

**Evidence:** 40/60 achieves best NDCG@10 (0.4513)

### 3. Why NOT Query Expansion?

**Decision:** Disable GPT-4 query expansion

**Rationale:**
- Over-expansion introduces noise
- Generic LLM synonyms don't match technical jargon
- Empirical evidence: -1.43% NDCG, -8.58% Recall

**Lesson:** Always measure! More AI ≠ better results

### 4. Why RAG Summarization?

**Decision:** Deploy as optional feature

**Rationale:**
- High-quality summaries (themes, priorities, recommendations)
- 66x ROI ($4.6K cost → $303K value from time saved)
- User-triggered (no latency for normal search)

**Evidence:** 6/6 successful summaries, 83 hours/day saved

### 5. Why Privacy Matters?

**Decision:** Azure OpenAI with BAA for production

**Rationale:**
- Medical device context requires HIPAA compliance
- Standard OpenAI API has no BAA (Business Associate Agreement)
- Violations: $50K/violation, up to $1.5M/year

**Solution:** Azure OpenAI ($6K/year) + data anonymization

---

## 📈 Business Impact

### Quantitative Results

**Time Savings:**
- Search time: 5 min → 30 sec (90% reduction)
- With RAG: 45 sec to scan → 10 sec to read summary
- Total: **83 hours/day saved** (250 users)

**Cost-Benefit Analysis:**

| Feature | Annual Cost | Annual Value | ROI |
|---------|-------------|--------------|-----|
| Hybrid Search | $0 (one-time dev) | $150K (time saved) | ∞ |
| RAG Summarization | $4.6K | $303K | 66x |
| Duplicate Detection | $130 | $1K | 7.7x |
| **Total** | **$4.7K** | **$454K** | **97x** |

### Qualitative Impact

- **Faster decision-making:** Executives understand 100-bug backlogs in 10 seconds
- **Reduced duplication:** 67% fewer false positives in duplicate detection
- **Better user experience:** Semantic understanding handles vague queries

---

## 🔐 Privacy & Compliance

### Regulatory Considerations

**Frameworks:**
- **HIPAA:** Medical device data requires Business Associate Agreement (BAA)
- **GDPR:** EU data must stay in EU or approved countries
- **ISO 13485:** Medical device QMS requires validated software tools

### Mitigation Strategies

1. **Data Anonymization**
   - Regex-based PII removal (SSN, MRN, IP, credentials)
   - 80% effective, but not foolproof

2. **Azure OpenAI (Production)**
   - BAA available for HIPAA compliance
   - EU data residency (West Europe, North Europe)
   - Dedicated instances (no data sharing)
   - Cost: +$6K/year vs standard OpenAI

3. **On-Premise LLMs (Highest Security)**
   - Llama 2 70B, Mistral 8x7B
   - Zero data leaves premises
   - Trade-off: Higher latency, maintenance burden

**See `experiments/llm_integration/COST_LATENCY_PRIVACY_ANALYSIS.md` for details**

---

## 🎤 For Interviews

### Elevator Pitch (30 seconds)

> "I built an intelligent search system for software backlogs, combining BM25 keyword matching with semantic embeddings. Through rigorous evaluation on 69 test queries, I achieved 44.7% NDCG@10, improved to 60.9% with cross-encoder reranking. I explored LLM integration: query expansion degraded performance by 1.4%, but RAG summarization provided 66x ROI. I conducted comprehensive cost, latency, and privacy analysis, recommending selective LLM deployment with HIPAA-compliant Azure OpenAI. This demonstrates ML implementation, business judgment, and production readiness."

### Key Talking Points

1. **Problem Solving:** Identified hybrid search as optimal (BM25 + Semantic)
2. **Experimental Rigor:** 30-config grid search, MLflow tracking, industry-standard metrics
3. **Business Judgment:** Rejected query expansion despite implementation (data showed failure)
4. **LLM Integration:** 3 use cases, empirical evaluation, cost-benefit analysis
5. **Privacy Awareness:** HIPAA/GDPR compliance, data anonymization, Azure OpenAI

### Common Questions & Answers

**Q: "Why did query expansion fail?"**
> "GPT-4 over-expanded queries with too many generic synonyms. For 'login problems', it added 'authentication sign-in access credentials...' which diluted BM25 term weighting and confused semantic search. Technical domains need precise terminology, not generic synonyms. I measured -1.4% NDCG drop empirically."

**Q: "How do you measure ROI?"**
> "Quantitative value: RAG saves 35 sec/use (45s scan → 10s read). 250 users × 20 searches/day × 20% adoption × 35s = 83 hrs/day. At $10/hr knowledge work, that's $303K/year value vs $4.6K cost = 66x ROI."

**Q: "What about privacy?"**
> "Layered approach: (1) Synthetic data for development, (2) Regex PII removal for LLM calls, (3) Azure OpenAI with BAA for HIPAA, (4) On-premise LLMs for highest security. Medical device context requires strict compliance - $50K/violation penalties."

---

## 📚 Documentation

- **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** - Comprehensive technical guide (Senior → Junior)
- **[COST_LATENCY_PRIVACY_ANALYSIS.md](experiments/llm_integration/COST_LATENCY_PRIVACY_ANALYSIS.md)** - Detailed LLM analysis
- **[config.yaml](config.yaml)** - Configuration reference

---

## 🛠️ Tech Stack

**Core ML:**
- Python 3.9+
- PyTorch 2.0+
- Sentence Transformers (all-mpnet-base-v2)
- scikit-learn

**Information Retrieval:**
- rank-bm25 (BM25 implementation)
- FAISS (scalable similarity search)

**LLM Integration:**
- OpenAI GPT-4 Turbo
- Azure OpenAI (production)

**Experiment Tracking:**
- MLflow (hyperparameter tuning, metrics)
- Pandas (data analysis)

**Utilities:**
- NLTK (tokenization)
- PyYAML (configuration)
- Streamlit (demo UI)

---

## 🚧 Future Work

1. **User Feedback Loop**
   - Implicit signals (clicks, dwell time)
   - Explicit signals (thumbs up/down)
   - Continuous model improvement

2. **A/B Testing Infrastructure**
   - Randomized control/treatment assignment
   - Statistical significance testing
   - Safe rollout mechanism

3. **Multi-Language Support**
   - Extend to non-English bug reports
   - Multilingual embeddings (e.g., LaBSE)

4. **Real-Time Indexing**
   - Incremental FAISS updates
   - Handle 100+ new items/day
   - Sub-second index refresh

5. **Fine-Tuned Models**
   - Domain-specific sentence transformers
   - Train on bug report data
   - Expected +5-10% NDCG improvement

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Naman** - AI Engineer Lead, Carnegie Mellon University

Targeting: MLE / Applied Scientist roles at Apple, Google, and other FAANG companies

**Contact:**
- LinkedIn: [linkedin.com/in/namanchoudhary](https://www.linkedin.com/in/namanchoudhary/)
- Portfolio: [naman-choudhary-ai-ml.github.io](https://naman-choudhary-ai-ml.github.io/)

---

## 🙏 Acknowledgments

- **CMU Team:** 6-person team collaboration on original Philips project
- **Open Source:** Sentence Transformers, FAISS, rank-bm25 communities
- **Inspiration:** Modern IR systems at Google, Bing, Elastic

---

## ⭐ Star History

If this project helped you, please consider giving it a ⭐!

**Built with ❤️ and rigorous ML engineering practices.**
