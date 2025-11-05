# Algorithms HW #3-2: implementing BST and Hash Table
- Author: Yeonjun Kim (2024-13755)
- Date: 2025-10-19
- Programmed and tested in Ubuntu 24.04 environment.

## Features
- BST_Node class
- HashTable and HashTable class
- insert_bst(root, key)
- search_bst(root, key)
- delete_bst(root, key)
- inorder_bst(root)
- preorder_bst(root)
- postorder_bst(root)
- insert_hash(hash_table, key)
- search_hash(hash_table, key)
- delete_hash(hash_table, key)

## How to run
- Before running the program, you should place `input.txt` and `op.txt` in this directory. In `input.txt`, you write the elements to push into the data structure, separated by a new line(`\n`). In `op.txt`, you write one data operation at a line. e.g. `INSERT 42`, `SEARCH 42`, `DELETE 42`. If either of these files are not present, the program will not work properly.
- For performance comparison(Part 3), the program will automatically generate the `tests/` directory and random test case inputs.
- You can run the program by `$ python3 202413755_Task3.py`, and see the results in `output_bst.txt`, `output_hash.txt`, and `performance_summary.txt`.