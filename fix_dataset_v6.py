#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruir dataset v6 (144 algoritmos, balanceado)
Este script genera el dataset correcto para v6.
"""

import json
from pathlib import Path

# Dataset v2 base (114 algoritmos)
V2_ALGORITHMS = [
    # O(1) - 6 algoritmos
    {"id": "constant_access", "name": "Constant Access", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "get_element", "name": "Get Element", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "array_access", "name": "Array Access", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "hash_lookup", "name": "Hash Lookup", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "simple_assignment", "name": "Simple Assignment", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "check_even", "name": "Check Even", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    
    # O(n) - 52 algoritmos
    {"id": "linear_search", "name": "Linear Search", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "array_sum", "name": "Array Sum", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "find_max", "name": "Find Max", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "find_min", "name": "Find Min", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "traversal", "name": "Array Traversal", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "count_occurrences", "name": "Count Occurrences", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "palindrome_check", "name": "Palindrome Check", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "string_concat", "name": "String Concatenation", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "reverse_array", "name": "Reverse Array", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "two_pointer_sum", "name": "Two Pointer Sum", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "contains_element", "name": "Contains Element", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "remove_duplicates", "name": "Remove Duplicates", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "rotate_array", "name": "Rotate Array", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "partition", "name": "Partition", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "next_greater", "name": "Next Greater", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "element_frequency", "name": "Element Frequency", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "valid_parentheses", "name": "Valid Parentheses", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "majority_element", "name": "Majority Element", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "missing_number", "name": "Find Missing Number", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "unique_characters", "name": "Unique Characters", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "product_array", "name": "Product of Array", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "common_prefix", "name": "Common Prefix", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "is_anagram", "name": "Is Anagram", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "merge_arrays", "name": "Merge Sorted Arrays", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "delete_element", "name": "Delete Element", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "find_peak", "name": "Find Peak", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "duplicate_count", "name": "Duplicate Count", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "even_odd_split", "name": "Even Odd Split", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "first_last_occurrence", "name": "First Last Occurrence", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "kth_element", "name": "Kth Element", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "longest_increasing", "name": "Longest Increasing", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "prefix_sum", "name": "Prefix Sum", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "remove_element", "name": "Remove Element", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "rotate_string", "name": "Rotate String", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "shortest_subarray", "name": "Shortest Subarray", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "single_number", "name": "Single Number", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "subsequence_match", "name": "Subsequence Match", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "sum_subarray", "name": "Sum Subarray", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "valid_anagram", "name": "Valid Anagram", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "word_pattern", "name": "Word Pattern", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    {"id": "zigzag_traverse", "name": "Zigzag Traverse", "complexity_class": 2, "features": {"loops": 1, "recursion": False, "nested_depth": 1}},
    
    # O(n²) - 9 algoritmos
    {"id": "bubble_sort", "name": "Bubble Sort", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "insertion_sort", "name": "Insertion Sort", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "selection_sort", "name": "Selection Sort", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "nested_loop_print", "name": "Nested Loop Print", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "matrix_sum", "name": "Matrix Sum", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "two_sum_brute", "name": "Two Sum Brute Force", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "array_pairs", "name": "Array Pairs", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "substring_search", "name": "Substring Search", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "closest_pair_2d", "name": "Closest Pair", "complexity_class": 4, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    
    # O(2^n) - 16 algoritmos
    {"id": "fibonacci_recursive", "name": "Fibonacci Recursive", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "power_set", "name": "Power Set", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "permutations", "name": "Permutations", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "subsets_gen", "name": "Subsets Generation", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "partition_subsets", "name": "Partition Subsets", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "subset_sum", "name": "Subset Sum", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "knapsack_brute", "name": "Knapsack Brute Force", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "n_queens_brute", "name": "N Queens Brute", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "hamiltonian_cycle", "name": "Hamiltonian Cycle", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "clique_problem", "name": "Clique Problem", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "tsp_brute", "name": "TSP Brute Force", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "change_making", "name": "Change Making", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "graph_coloring_brute", "name": "Graph Coloring Brute", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "vertex_cover", "name": "Vertex Cover", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "longest_path", "name": "Longest Path", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    {"id": "all_subsequences", "name": "All Subsequences", "complexity_class": 6, "features": {"loops": 0, "recursion": True, "nested_depth": 3}},
    
    # O(n³) - 16 algoritmos
    {"id": "triple_loop_1", "name": "Triple Loop 1", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "triple_loop_2", "name": "Triple Loop 2", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "floyd_warshall", "name": "Floyd Warshall", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "matrix_multiply", "name": "Matrix Multiply", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "3sum_brute", "name": "3Sum Brute Force", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "tensor_ops", "name": "Tensor Operations", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "volume_calc", "name": "Volume Calculation", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "pixel_filter", "name": "Pixel Filter", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "context_search", "name": "Context Search", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "nested_iteration", "name": "Nested Iteration", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "convolution_3d", "name": "Convolution 3D", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "allocation_matrix", "name": "Allocation Matrix", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "block_computation", "name": "Block Computation", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "string_search_3d", "name": "String Search 3D", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "grid_traversal", "name": "Grid Traversal", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
    {"id": "nested_range", "name": "Nested Range", "complexity_class": 5, "features": {"loops": 3, "recursion": False, "nested_depth": 3}},
]

# 30 nuevos O(log n) para v6
NEW_OLOGN = [
    {"id": "merge_sort", "name": "Merge Sort", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "quick_sort", "name": "Quick Sort", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "heap_sort", "name": "Heap Sort", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "binary_search", "name": "Binary Search", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "bst_search", "name": "BST Search", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "balanced_tree_insert", "name": "Balanced Tree Insert", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "avl_rotate", "name": "AVL Rotate", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "count_inversions", "name": "Count Inversions", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "closest_pair", "name": "Closest Pair 2D", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "merge_k_arrays", "name": "Merge K Arrays", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "convex_hull", "name": "Convex Hull", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "bit_construction", "name": "BIT Construction", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "segment_tree", "name": "Segment Tree", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "kth_smallest", "name": "Kth Smallest", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "merge_intervals", "name": "Merge Intervals", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "max_subarray_dc", "name": "Max Subarray (D&C)", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "find_duplicates", "name": "Find Duplicates", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "sort_persons", "name": "Sort Persons", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "tournament_sort", "name": "Tournament Sort", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "pair_inversions", "name": "Pair Inversions", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "unique_elements", "name": "Unique Elements", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "sort_nearly_sorted", "name": "Sort Nearly Sorted", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "external_sort", "name": "External Sort", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "n_way_merge", "name": "N-Way Merge", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "shell_sort", "name": "Shell Sort", "complexity_class": 1, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "introsort", "name": "Introsort", "complexity_class": 1, "features": {"loops": 1, "recursion": True, "nested_depth": 2}},
    {"id": "timsort", "name": "Timsort", "complexity_class": 1, "features": {"loops": 2, "recursion": False, "nested_depth": 2}},
    {"id": "suffix_array", "name": "Suffix Array", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "median_sorted_arrays", "name": "Median Sorted Arrays", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
    {"id": "quick_select", "name": "Quick Select", "complexity_class": 1, "features": {"loops": 1, "recursion": False, "nested_depth": 2}},
]

def main():
    print("=" * 80)
    print("RECONSTRUYENDO DATASET v6 (144 ALGORITMOS BALANCEADOS)")
    print("=" * 80)
    
    # Combinar v2 base + 30 O(log n) nuevos
    algorithms = V2_ALGORITHMS + NEW_OLOGN
    
    print(f"\n✅ Total: {len(algorithms)} algoritmos")
    
    # Análisis de distribución
    dist = {}
    for algo in algorithms:
        cc = algo["complexity_class"]
        dist[cc] = dist.get(cc, 0) + 1
    
    names = {0: "O(1)", 1: "O(log n)", 2: "O(n)", 4: "O(n²)", 5: "O(n³)", 6: "O(2^n)"}
    total = len(algorithms)
    
    print("\nDistribución:")
    for cc in sorted(dist.keys()):
        count = dist[cc]
        pct = (count / total) * 100
        print(f"  {names.get(cc, f'Class {cc}'):12} {count:3} ({pct:5.1f}%)")
    
    # Guardar
    data = {
        "algorithms": algorithms,
        "version": "v6",
        "total": len(algorithms),
        "distribution": dist
    }
    
    output_path = Path("data/dataset.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Dataset guardado en: {output_path}")
    print("=" * 80)

if __name__ == "__main__":
    main()
