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
    graph_labels = pd.read_csv(os.path.join(dataset_path, 'graph_labels.csv.gz'), header = None)
    num_nodes = pd.read_csv(os.path.join(dataset_path, 'num_nodes.csv.gz'), header = None)
    num_edges = pd.read_csv(os.path.join(dataset_path, 'num_edges.csv.gz'), header = None)
    edges = pd.read_csv(os.path.join(dataset_path, 'edges.csv.gz'), header = None)
    node_features = pd.read_csv(os.path.join(dataset_path, 'node_features.csv.gz'), header = None)
    edge_features = pd.read_csv(os.path.join(dataset_path, 'edge_features.csv.gz'), header = None)
    
    nodes_line = 0
    edges_line = 0
    dataset = []
    num_1 = 0
    total = 0
    for index, row in graph_labels.iterrows():
        n = num_nodes.iloc[index][0]
        m = num_edges.iloc[index][0]
        y = graph_labels.iloc[index][0]
        edge = torch.LongTensor(edges.iloc[edges_line:edges_line + m].values.tolist())
        nf = torch.tensor(node_features.iloc[nodes_line:nodes_line + n].values.tolist(), dtype = torch.long)
        ef = torch.tensor(edge_features.iloc[edges_line:edges_line + m].values.tolist(), dtype = torch.long)
        nodes_line += n
        edges_line += m
        if(np.isnan(y)):
            continue
        num_1 += y
        total += 1
        if len(edge) == 0:
            print(ef, y)
            data = Data(x = nf, edge_index = torch.LongTensor([]), edge_attr = ef, y = torch.Tensor([y]))
            dataset.append(data)
        else:
            data = Data(x = nf, edge_index = edge.T, edge_attr = ef, y = torch.Tensor([y]))
            dataset.append(data)
    return dataset, num_1, total

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.node_dim = 16
        self.edge_dim = 2
        self.node_encoder = NodeEncoder(self.node_dim)
        self.edge_encoder = EdgeEncoder(self.edge_dim)
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

def train(loader, batch_size):
    model.train()
    loss_all = 0
    for data in loader:
        optimizer.zero_grad()
        output = model(data).float()
        label = torch.reshape(data.y, (-1, 1))
        loss = crit(output, label)
        loss.backward()
        loss_all += loss.item()#*data.num_graphs
        optimizer.step()
    return loss_all

def evaluate(loader):
    model.eval()
    with torch.no_grad():
        predictions = []
        actual = []
        for data in loader:
            pred = (torch.sigmoid(model(data))).float().flatten()
            label = data.y
            predictions.extend(pred.numpy())
            actual.extend(label.numpy())
        acc = (torch.Tensor(predictions) == torch.Tensor(actual)).sum()/len(torch.Tensor(predictions))
        roc_auc = roc_auc_score(torch.Tensor(actual), torch.Tensor(predictions))
        bce_loss = crit(torch.Tensor(predictions), torch.Tensor(actual))
        return bce_loss, acc, roc_auc
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Training a classification model")
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--dataset_path", required=True)
    parser.add_argument("--val_dataset_path", required=True)
    args = parser.parse_args()
    print(f"Training a classification model. Output will be saved at {args.model_path}. Dataset will be loaded from {args.dataset_path}. Validation dataset will be loaded from {args.val_dataset_path}.")
    
    batch_size = 64
    train_data, num_1,total  = create_data(args.dataset_path)
    train_loader = DataLoader(train_data, batch_size = batch_size)

    val_data, _, _ = create_data(args.val_dataset_path)
    val_loader = DataLoader(val_data, batch_size = batch_size)

    model = Net()
    optimizer = torch.optim.Adam(model.parameters(), lr = 0.01, weight_decay = 5e-4)
    crit = torch.nn.BCEWithLogitsLoss(pos_weight = torch.Tensor([(total - num_1) / num_1]))
    epochs = 150
    model.train()
    
    best_roc = 0
    train_roc_list = []
    train_loss_list = []
    val_roc_list = []
    val_loss_list = []
    for epoch in range(epochs):
        loss = train(train_loader, batch_size)
        train_loss, train_acc, train_roc = evaluate(train_loader)
        val_loss, val_acc, val_roc = evaluate(val_loader)
        if val_roc > best_roc:
            best_roc = val_roc
            best_model = copy.deepcopy(model)
        train_roc_list.append(train_roc)
        train_loss_list.append(train_loss)
        val_roc_list.append(val_roc)
        val_loss_list.append(val_loss)
        print(epoch, train_loss, train_roc, val_loss, val_roc)
    torch.save(best_model.state_dict(), args.model_path)

    x = [i for i in range(epochs)]
    plt.plot(x, train_roc_list, label = 'Train')
    plt.plot(x, val_roc_list, label = 'Val')
    plt.title('ROC-AUC vs Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('ROC-AUC')
    plt.legend()
    plt.savefig('Q1_roc_auc.png')

    plt.clf()
    plt.plot(x, train_loss_list, label = 'Train')
    plt.plot(x, val_loss_list, label = 'Val')
    plt.title('Loss vs Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig('Q1_loss.png')