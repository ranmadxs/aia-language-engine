import tensorflow_decision_forests as tfdf
import tensorflow as tf

# Create the model builder
builder = tfdf.builder.RandomForestBuilder(
    path="/tmp/manual_model",
    objective=tfdf.py_tree.objective.ClassificationObjective(
        label="color", classes=["red", "blue", "green"]))

# So alias
Tree = tfdf.py_tree.tree.Tree
SimpleColumnSpec = tfdf.py_tree.dataspec.SimpleColumnSpec
ColumnType = tfdf.py_tree.dataspec.ColumnType
# Nodes
NonLeafNode = tfdf.py_tree.node.NonLeafNode
LeafNode = tfdf.py_tree.node.LeafNode
# Conditions
NumericalHigherThanCondition = tfdf.py_tree.condition.NumericalHigherThanCondition
CategoricalIsInCondition = tfdf.py_tree.condition.CategoricalIsInCondition
# Leaf values
ProbabilityValue = tfdf.py_tree.value.ProbabilityValue

builder.add_tree(
    Tree(
        NonLeafNode(
            condition=NumericalHigherThanCondition(
                feature=SimpleColumnSpec(name="f1", type=ColumnType.NUMERICAL),
                threshold=1.5,
                missing_evaluation=False),
            pos_child=NonLeafNode(
                condition=CategoricalIsInCondition(
                    feature=SimpleColumnSpec(name="f2",type=ColumnType.CATEGORICAL),
                    mask=["cat", "dog"],
                    missing_evaluation=False),
                pos_child=LeafNode(value=ProbabilityValue(probability=[0.8, 0.1, 0.1], num_examples=10)),
                neg_child=LeafNode(value=ProbabilityValue(probability=[0.1, 0.8, 0.1], num_examples=20))),
            neg_child=LeafNode(value=ProbabilityValue(probability=[0.1, 0.1, 0.8], num_examples=30)))))

builder.close()
manual_model = tf.keras.models.load_model("/tmp/manual_model")

examples = tf.data.Dataset.from_tensor_slices({
        "f1": [1.0, 2.0, 3.0],
        "f2": ["cat", "cat", "bird"]
    }).batch(2)

predictions = manual_model.predict(examples)

print("predictions:\n",predictions)

yggdrasil_model_path = manual_model.yggdrasil_model_path_tensor().numpy().decode("utf-8")
print("yggdrasil_model_path:",yggdrasil_model_path)

inspector = tfdf.inspector.make_inspector(yggdrasil_model_path)
print("Input features:", inspector.features())

tfdf.model_plotter.plot_model_in_colab(manual_model)