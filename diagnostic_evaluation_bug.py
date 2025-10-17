"""
Diagnostic script to find the evaluation bug.

We have two evaluations using the same test set and same 50/50 fusion:
- Baseline evaluation: NDCG@10 = 0.4473
- Cross-encoder baseline: NDCG@10 = 0.5983

This script will:
1. Load both search systems
2. Run the same query through both
3. Compare results step-by-step
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
from evaluation.evaluate_baseline import build_search_system, search_hybrid, load_test_set
from evaluation.metrics.ranking_metrics import aggregate_metrics

# Also load cross-encoder search function
from experiments.advanced_retrieval.cross_encoder.reranking import load_search_system as load_ce_system, retrieve_candidates_hybrid

def main():
    print("="*80)
    print("DIAGNOSTIC: Finding Evaluation Bug")
    print("="*80)

    # Load data
    print("\n1. Loading data...")
    backlog_df = pd.read_csv("evaluation/synthetic_data/synthetic_backlog.csv")
    test_set = load_test_set(Path("evaluation/test_sets/test_set_compact.csv"))

    # Build both search systems
    print("\n2. Building search systems...")
    baseline_system = build_search_system(backlog_df)
    ce_system = load_ce_system()

    # Pick one query to test
    test_query = list(test_set.keys())[0]
    print(f"\n3. Testing query: '{test_query}'")

    # Get baseline results
    print("\n4. Baseline evaluation method:")
    baseline_ids, baseline_scores = search_hybrid(
        test_query,
        baseline_system,
        bm25_weight=0.5,
        semantic_weight=0.5,
        top_k=10
    )
    print(f"   Top 10 doc IDs: {baseline_ids}")
    print(f"   Scores: {baseline_scores}")

    # Get cross-encoder baseline results
    print("\n5. Cross-encoder baseline method:")
    ce_results = retrieve_candidates_hybrid(test_query, ce_system, top_k=10)
    ce_ids = ce_results['ID'].tolist()
    ce_scores = ce_results['retrieval_score'].tolist()
    print(f"   Top 10 doc IDs: {ce_ids}")
    print(f"   Scores: {ce_scores}")

    # Compare
    print("\n6. Comparison:")
    if baseline_ids == ce_ids:
        print("   ✓ Document rankings are IDENTICAL")
    else:
        print("   ✗ Document rankings are DIFFERENT!")
        print(f"\n   Baseline only: {set(baseline_ids) - set(ce_ids)}")
        print(f"   CE only: {set(ce_ids) - set(baseline_ids)}")

    # Now compute NDCG for all queries using both methods
    print("\n7. Computing NDCG@10 for all queries using both methods...")

    baseline_relevances = []
    ce_relevances = []
    baseline_totals = []
    ce_totals = []
    baseline_ground_truth = []
    ce_ground_truth = []

    for query, data in test_set.items():
        doc_to_relevance = {doc_id: rel for doc_id, rel in zip(data['document_ids'], data['relevances'])}
        total_relevant = sum(1 for rel in data['relevances'] if rel > 0)

        # Ground truth relevances from test set
        ground_truth_rels = data['relevances']

        # Baseline method
        baseline_ids, _ = search_hybrid(query, baseline_system, 0.5, 0.5, top_k=10)
        baseline_rels = [doc_to_relevance.get(doc_id, 0) for doc_id in baseline_ids]
        baseline_relevances.append(baseline_rels)
        baseline_totals.append(total_relevant)
        baseline_ground_truth.append(ground_truth_rels)

        # CE method
        ce_results = retrieve_candidates_hybrid(query, ce_system, top_k=10)
        ce_ids = ce_results['ID'].tolist()
        ce_rels = [doc_to_relevance.get(doc_id, 0) for doc_id in ce_ids]
        ce_relevances.append(ce_rels)
        ce_totals.append(total_relevant)
        ce_ground_truth.append(ground_truth_rels)

    # Compute aggregate metrics
    baseline_metrics = aggregate_metrics(baseline_relevances, baseline_totals, k_values=[10], all_ground_truth_relevances=baseline_ground_truth)
    ce_metrics = aggregate_metrics(ce_relevances, ce_totals, k_values=[10], all_ground_truth_relevances=ce_ground_truth)

    print("\n8. Results:")
    print(f"   Baseline method NDCG@10: {baseline_metrics['ndcg@10']:.6f}")
    print(f"   CE method NDCG@10:       {ce_metrics['ndcg@10']:.6f}")
    print(f"   Difference:              {abs(baseline_metrics['ndcg@10'] - ce_metrics['ndcg@10']):.6f}")

    if abs(baseline_metrics['ndcg@10'] - ce_metrics['ndcg@10']) < 0.001:
        print("\n✓ NDCG values match! No bug.")
    else:
        print("\n✗ NDCG values DON'T match! BUG CONFIRMED.")
        print("\nLet me check a few queries in detail...")

        # Find queries with biggest differences
        for i, (query, data) in enumerate(list(test_set.items())[:5]):
            print(f"\nQuery {i+1}: '{query}'")
            print(f"  Baseline relevances: {baseline_relevances[i]}")
            print(f"  CE relevances:       {ce_relevances[i]}")
            if baseline_relevances[i] != ce_relevances[i]:
                print("  ⚠️  DIFFERENT!")

if __name__ == "__main__":
    main()
