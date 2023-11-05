import pandas as pd
import numpy as np
import json
from scipy.sparse import csr_matrix
import networkx as nx
import matplotlib.pyplot as plt
import Dataset as ds


def matrix_creation(df, save = True, path="data/"):
    rows, cols, data = [], [], []
    
    for i in range(len(df)):
        for ref in df["references"][i]:
            # if ref doesn't exist in df, skip and store the missing ref
            if ref not in df["link"].values:
                print(ref)
                continue
            else:
                rows.append(i)
                cols.append(df[df["link"]==ref].index[0])
                data.append(1)
    
    adjacency_matrix = csr_matrix((data, (rows, cols)), shape=(len(df), len(df)))
    
    if save:
        np.save(f'{path}adjacency_matrix_data.npy', adjacency_matrix.data)
        np.save(f'{path}adjacency_matrix_indices.npy', adjacency_matrix.indices)
        np.save(f'{path}adjacency_matrix_indptr.npy', adjacency_matrix.indptr)
    
    return adjacency_matrix

                 
df = ds.dataset_loop(loop = False)

matrix = matrix_creation(df)

# data = np.load('data/adjacency_matrix_data.npy')
# indices = np.load('data/adjacency_matrix_indices.npy')
# indptr = np.load('data/adjacency_matrix_indptr.npy')

# adjacency_matrix = csr_matrix((data, indices, indptr), shape=(len(indptr) - 1, max(indices) + 1))



# # continue in R
# install.packages("reticulate")
# install.packages("Matrix")

# library(reticulate)
# library(Matrix)

# use_python("C:/Users/Aless/AppData/Local/Programs/Python/Python311/python.exe", required = TRUE)

# data <- npyLoad("data/adjacency_matrix_data.npy")
# indices <- npyLoad("data/adjacency_matrix_indices.npy")
# indptr <- npyLoad("data/adjacency_matrix_indptr.npy")

# adjacency_matrix <- sparseMatrix(i = indices + 1, j = indptr + 1, x = data, dims = c(length(indptr) - 1, max(indices) + 1))

