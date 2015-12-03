####USE

Here is a step-by-step example to illustrate compare_classifiers module.

```python
import Tools.agd_tools.compare_classifiers.tree as tree
import Tools.agd_tools.compare_classifiers.transformers as transformers

# -- Add the tasks you want to execute
tasks = [
    (feature_choice_1, feature_selection_1, classifier_1),
    (feature_choice_1, feature_selection_1, classifier_2),
    (feature_choice_1, feature_selection_2, classifier_2),
    (feature_choice_1, feature_selection_2, classifier_1)
    ]

# -- Root -> Import data
root = tree.Node(import_data_0)

# -- Build the tree
for task in tasks:
    root.add_leaf(task)
    
# deep-first-search (process Tree & execute)
root.deep_first_search_execute(None)

# deep-first-search (process Tree & print)
result_list = []
genealogy = []
root.depth_first_search_print(result_list, genealogy)

# Output results in a sexy-way
outputres = tree.OutputResults(result_list)  # Class instance
outputres.compute_result_table(result_list)
outputres.output_best_clf(result_list)


```

###TODO 

- Clear resultats table [OK]
- Add doc to tree.py
- Implement Hyperparametrisation in transformers.py
- Implement _param_choice_ in t Classifiers & FeatureSelection transformers.
- Unit tests
- Draw tree

