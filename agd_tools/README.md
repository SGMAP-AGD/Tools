####USE

```python
import Tools.agd_tools.compare_classifiers.tree as tree
import Tools.agd_tools.compare_classifiers.transformers as transformers

# -- Add the tasks you want to execute
tasks = [
    (choice_meteo_tr, selection_rf_1_tr, rf_classifier_tr),
    (choice_meteo_tr, selection_lr_tr, lr_classifier_tr),
    (choice_sansmeteo_tr, selection_rf_1_tr, rf_classifier_tr),
    (choice_sansmeteo_tr, selection_lr_tr, lr_classifier_tr)
    ]

# -- Root -> Import data
root = tree.Node(import_tr)

# -- Build the tree
for task in tasks:
    root.add_leaf(task)
    
# deep-first-search (process Tree & print results)
root.deep_first_search(None)

```

###TODO 

- Clear resultats table
- Add doc to Node.py
- Implement Hyperparametrisation in transformers.py
- Implement _param_choice_ in t Classifiers & FeatureSelection transformers.
- Unit tests
- Draw tree

