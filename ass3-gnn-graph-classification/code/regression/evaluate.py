import argparse
import pandas as pd
import numpy as np
import sys
import torch
from torch_geometric.data import Data
from torch.nn import Sequential as Seq, Linear, ReLU
from torch_geometric.loader import DataLoader
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import remove_self_loops, add_self_loops, dense_to_sparse
from torch_geometric.nn import TopKPooling, GATConv, SAGEConv, GCNConv
from torch_geometric.nn import global_mean_pool as gap, global_max_pool as gmp, SAGPooling
import torch.nn.functional as F
from torch_geometric.data import InMemoryDataset
from encoder import NodeEncoder, EdgeEncoder
from sklearn.metrics import roc_auc_score
import os
import copy
from matplotlib import pyplot as plt

def create_data(dataset_path):
    num_nodes = pd.read_csv(os.path.join(dataset_path, 'num_nodes.csv.gz'), header = None)
    num_edges = pd.read_csv(os.path.join(dataset_path, 'num_edges.csv.gz'), header = None)
    edges = pd.read_csv(os.path.join(dataset_path, 'edges.csv.gz'), header = None)
    node_features = pd.read_csv(os.path.join(dataset_path, 'node_features.csv.gz'), header = None)
    edge_features = pd.read_csv(os.path.join(dataset_path, 'edge_features.csv.gz'), header = None)
    
    nodes_line = 0
    edges_line = 0
    dataset = []
    for index, row in num_nodes.iterrows():
        n = num_nodes.iloc[index][0]
        m = num_edges.iloc[index][0]
        edge = torch.LongTensor(edges.iloc[edges_line:edges_line + m].values.tolist())
        nf = torch.tensor(node_features.iloc[nodes_line:nodes_line + n].values.tolist(), dtype = torch.long)
        ef = torch.tensor(edge_features.iloc[edges_line:edges_line + m].values.tolist(), dtype = torch.long)
        nodes_line += n
        edges_line += m
        if len(edge) == 0:
            data = Data(x = nf, edge_index = torch.LongTensor([]), edge_attr = ef)
            dataset.append(data)
        else:
            data = Data(x = nf, edge_index = edge.T, edge_attr = ef)
            dataset.append(data)
    return dataset

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.node_dim = 16
        self.edge_dim = 2
        self.node_encoder = NodeEncoder(self.node_dim)
        self.edge_encoder = EdgeEncoder(self.edge_dim)
        self.premlp = torch.nn.Linear(self.node_dim, 16)
        self.conv1 = GATConv(self.node_dim, 32, edge_dim = self.edge_dim)
        self.conv2 = GATConv(32, 32, edge_dim = self.edge_dim)
        self.conv3 = GATConv(32, 32, edge_dim = self.edge_dim)
        self.l3 = torch.nn.Linear(32*3, 1)
  
    def forward(self, data): 
        x, edge_index, ef = data.x, data.edge_index, data.edge_attr

        x = self.node_encoder(x)
        ef = self.edge_encoder(ef)
        x1 = self.conv1(x, edge_index, edge_attr = ef)
        x2 = self.conv2(x1, edge_index, edge_attr = ef)
        x3 = self.conv3(x2, edge_index, edge_attr = ef)

        x_cat = torch.cat((x1, x2, x3), 1)
        x = gap(x_cat, data.batch)
        xl3 = self.l3(x)

        return xl3

def tocsv(y_arr, *, task):
    r"""Writes the numpy array to a csv file.
    params:
        y_arr: np.ndarray. A vector of all the predictions. Classes for
        classification and the regression value predicted for regression.

        task: str. Must be either of "classification" or "regression".
        Must be a keyword argument.
    Outputs a file named "y_classification.csv" or "y_regression.csv" in
    the directory it is called from. Must only be run once. In case outputs
    are generated from batches, only call this output on all the predictions
    from all the batches collected in a single numpy array. This means it'll
    only be called once.

    This code ensures this by checking if the file already exists, and does
    not over-write the csv files. It just raises an error.

    Finally, do not shuffle the test dataset as then matching the outputs
    will not work.
    """
    import os
    import numpy as np
    import pandas as pd
    assert task in ["classification", "regression"], f"task must be either \"classification\" or \"regression\". Found: {task}"
    assert isinstance(y_arr, np.ndarray), f"y_arr must be a numpy array, found: {type(y_arr)}"
    assert len(y_arr.squeeze().shape) == 1, f"y_arr must be a vector. shape found: {y_arr.shape}"
    assert not os.path.isfile(f"y_{task}.csv"), f"File already exists. Ensure you are not calling this function multiple times (e.g. when looping over batches). Read the docstring. Found: y_{task}.csv"
    y_arr = y_arr.squeeze()
    df = pd.DataFrame(y_arr)
    df.to_csv(f"y_{task}.csv", index=False, header=False)

def evaluate(loader):
    model.eval()
    with torch.no_grad():
        predictions = []
        for data in loader:
            pred = model(data).float().flatten()
            predictions.extend(pred.numpy())
    numpy_ys = np.asarray(predictions)
    tocsv(numpy_ys, task = "regression") 

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Evaluating the classification model")
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--dataset_path", required=True)
    args = parser.parse_args()
    print(f"Evaluating the classification model. Model will be loaded from {args.model_path}. Test dataset will be loaded from {args.dataset_path}.")

    test_data = create_data(args.dataset_path)
    test_loader = DataLoader(test_data, 64)

    model = Net()
    model.load_state_dict(torch.load(args.model_path, map_location=torch.device('cpu')))
    evaluate(test_loader)
