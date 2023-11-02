import tensorflow_decision_forests as tfdf

import os
import numpy as np
import pandas as pd
import tensorflow as tf
import math
import collections

try:
  from wurlitzer import sys_pipes
except:
  from colabtools.googlelog import CaptureLog as sys_pipes

from IPython.core.magic import register_line_magic
from IPython.display import Javascript


# Load a dataset into a Pandas Dataframe.
dataset_df = pd.read_csv("penguins.csv")

# Show the first three examples.
print(dataset_df.head(3))

# Convert the pandas dataframe into a tf dataset.
dataset_tf = tfdf.keras.pd_dataframe_to_tf_dataset(dataset_df, label="species")

# Train the Random Forest
model = tfdf.keras.RandomForestModel(compute_oob_variable_importances=True)
model.fit(x=dataset_tf)

model.summary()

tfdf.model_plotter.plot_model_in_colab(model)

'''
inspector = model.make_inspector()

[field for field in dir(inspector) if not field.startswith("_")]

print("Model type:", inspector.model_type())
print("Number of trees:", inspector.num_trees())
print("Objective:", inspector.objective())
print("Input features:", inspector.features())

inspector.evaluation()

print(f"Available variable importances:")
for importance in inspector.variable_importances().keys():
  print("\t", importance)

inspector.variable_importances()["MEAN_DECREASE_IN_AUC_1_VS_OTHERS"]

inspector.extract_tree(tree_idx=0)

# number_of_use[F] will be the number of node using feature F in its condition.
number_of_use = collections.defaultdict(lambda: 0)

# Iterate over all the nodes in a Depth First Pre-order traversals.
for node_iter in inspector.iterate_on_nodes():

  if not isinstance(node_iter.node, tfdf.py_tree.node.NonLeafNode):
    # Skip the leaf nodes
    continue

  # Iterate over all the features used in the condition.
  # By default, models are "oblique" i.e. each node tests a single feature.
  for feature in node_iter.node.condition.features():
    number_of_use[feature] += 1

print("Number of condition nodes per features:")
for feature, count in number_of_use.items():
  print("\t", feature.name, ":", count)

'''