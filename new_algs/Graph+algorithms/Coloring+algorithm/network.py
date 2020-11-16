# Includes Single Deep-Q Network and Double Deep-Q Network Structures
# Main Network File for Reinforcement Learning Application on Graph Coloring Problem

import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import random

from graph.graph_lib import Graph_Lib

class QNet(nn.Module):

    def __init__(self, input_dims, lr):
        super(QNet, self).__init__()
        # gpu or cpu set
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu') # running on cpu or single gpu
        self.to(self.device)
        # network parameters
        self.hidden_layer_neurons = 512
        # layers
        self.fc1 = nn.Linear(input_dims, self.hidden_layer_neurons) # 2 layer fully connected network structure
        self.fc2 = nn.Linear(self.hidden_layer_neurons, 1)
        self.optimizer = optim.RMSprop(self.parameters(), lr=lr) # optimizer chosen as RMSProp
        self.loss = nn.MSELoss() # loss chosen as Mean Squared Error

    def forward(self, state):
        fc1 = F.relu(self.fc1(state))
        action = torch.sigmoid(self.fc2(fc1))
        return action
    
    def save_model(self, path):
        torch.save(self.state_dict(), path)
    
    def load_model(self, path):
        self.load_state_dict(torch.load(path))
    
class DoubleQNet():

    def __init__(self, input_dims, learning_rate, load_path=None):
        # learning parameters
        self.learning_rate = learning_rate
        self.step_counter = 0
        self.gamma = 0.9
        self.epsilon = 1
        self.epsilon_decay = 0.96
        # double deep learning Q networks
        self.local_qnet = QNet(input_dims, learning_rate)   # learning network
        self.target_qnet = QNet(input_dims, learning_rate)  # network following from the back

        if(load_path != None): # for evaluation or further training, pretrained models can be loaded
            self.local_qnet.load_model(load_path + 'local_qnet.params')
            self.target_qnet.load_model(load_path + 'target_qnet.params')

    
    def evaluate(self, path): 
        # Real folder path is given, in where there are only graph files. 
        # All the graphs in the folder are taken as a single batch.
        graphs = Graph_Lib()
        node_cnts = graphs.read_batch(path)         # all graphs are read
        filenames = graphs.get_batch_filenames()    # filenames of all graphs in batch are taken
        batch = len(node_cnts) # number of graphs are taken as batch number
        # embedding initialization
        graphs.init_node_embeddings()
        graphs.init_graph_embeddings()  
        # parameter initialization
        colored_arrs = []   # for each graph in batch, colored information of each node is preserved
        max_node = -1       # maximum node count
        avg_node = 0        # average node count
        for cnt in node_cnts:
            avg_node += cnt
            if(cnt > max_node):
                max_node = cnt
            colored_arrs.append([False]*cnt)
        max_colors = [-1]*batch
        avg_node /= batch
        
        for colored_cnt in range(max_node): # until coloring all the nodes in all the graphs
            print("Number of Nodes Colored:", colored_cnt)
            # decides which nodes to color for each graph
            actions, _, _ = self.decide_node_coloring(graphs, node_cnts, batch, colored_arrs, colored_cnt, evaluate=True)
            # colors the selected nodes stored in actions
            colors = graphs.color_batch(actions)
            # sets max color for graphs to color in this step if the selected color is bigger than max color
            _ = self.get_rewards(batch, colors, max_colors)
            if(colored_cnt % 3 == 0): # updates graph embeddings at every 3 steps
                graphs.update_graph_embeddings()
        
        for f, c in zip(filenames, max_colors): # prints results
            print(f, ",", c+1)
        
        return max_colors
    
    def train(self, epochs, batch_size, min_nodes, max_nodes, path=None):
        # model is trained, if a path is set, then a batch from all the files in this path is set
        # otherwise random graphs are constructed within the node range 
        for epoch in range(1, epochs + 1): # for each epoch
            loss_total = 0
            graphs = Graph_Lib()
            
            if(path != None): # if a path is set
                node_cnts = graphs.read_batch(path)
                batch = len(node_cnts) # number of graphs are taken as batch number
            else: # if no path is set
                batch = batch_size
                node_cnts = graphs.insert_batch(batch, min_nodes, max_nodes)
            
            # embedding initialization
            graphs.init_node_embeddings()
            graphs.init_graph_embeddings()
            
            # parameter initialization
            colored_arrs = []   # for each graph in batch, coloring informationf of each node is stored
            max_node = -1       # maximum nomber of nodes in the batch
            avg_node = 0        # average number of nodes in the batch
            for cnt in node_cnts:
                avg_node += cnt
                if(cnt > max_node):
                    max_node = cnt
                colored_arrs.append([False]*cnt)
            
            max_colors = [-1]*batch # max colors assigned for each graph in the batch are stored
            avg_node /= batch
            reward_last = np.zeros((3, batch)) # last 3 coloring steps' rewards are stored
            
            for colored_cnt in range(max_node): # until each node in each graph becomes colored
                # for each graph, nodes to color is seleced and stored in actions parameter
                actions, q_pred, not_finished = self.decide_node_coloring(graphs, node_cnts, batch, colored_arrs, colored_cnt)
                colors = graphs.color_batch(actions) # regarding to the selected actions (nodes), graphs are colored
                reward_last[colored_cnt % 3] = self.get_rewards(batch, colors, max_colors) # rewards for each graph are calculated for this step
                rewards = np.sum(reward_last, axis = 0) # last 3 steps' rewards are added and average of the mare taken
                rewards /= reward_last.shape[0]
                q_target = self.get_loss(graphs, batch, rewards, actions) # loss is calculated for the selected actions
                loss = self.local_qnet.loss(q_target, q_pred).to(self.local_qnet.device) # general lose is calculated and network is propogated backwards
                loss.backward()
                loss_total += loss / not_finished # average loss of unfinished graphs is calculated
                self.local_qnet.optimizer.step() 
                self.step_counter += 1
                if(colored_cnt % 3 == 0): # at every 3 steps, graph embeddings are updated
                    graphs.update_graph_embeddings()
            
            loss_total /= max_node # loss per node from whole coloring process is calculated
            print("Epoch:", epoch, "--- Loss:", loss_total) 
            graphs.reset_batch()
            if(self.epsilon > 0.05): # decay epsilon
                    self.epsilon *= self.epsilon_decay
            
            if(epoch % 10 == 0): # set target as local
                self.target_qnet.load_state_dict(self.local_qnet.state_dict())  
            
            if(epoch % 60 == 0):
                self.local_qnet.save_model('./backup/local_qnet' + str(epoch) + '.params')
                self.target_qnet.save_model('./backup/target_qnet' + str(epoch) + '.params')
                

            
    def decide_node_coloring(self, graphs, node_cnt, batch, colored_arrs, colored_cnt, evaluate=False):
        actions = []
        q_pred = []
        not_finished = batch
        for el in range(batch): # for each graph in batch:
            max_action = -9999
            max_node = -1
            # embeddings for nodes and graph is retrieved
            node_embeds = graphs.get_node_embed(el)
            graph_embeds = graphs.get_graph_embed(el)
            if(colored_cnt >= node_cnt[el]):
                # if a graph is finished coloring, then -1 is appended as action.
                # in C++, if action is seen as -1, no coloring will be made
                not_finished -= 1
                actions.append(-1)
                continue
            elif evaluate or random.random() > self.epsilon: # with the probability of 1-epsilon, network determines node to color
                node_np = np.array(node_embeds[:,6]) # incidence ordering (dynamic ordering) values for each node is taken
                node_np = node_np.argsort()[-10:][::-1] # nodes with maximum 10 incidence ordering values are chosen
                for node in node_np: # for each node selected above
                    if colored_arrs[el][node]:
                        continue
                    embeddings = np.concatenate([node_embeds[node], graph_embeds]) # final embedding is created
                    embeddings = torch.from_numpy(embeddings).float()
                    with torch.no_grad():
                        action = self.local_qnet(embeddings) # action value from the network for the current node is got
                    if(max_action < action): # node with the maximum action is saved
                        max_node = node
                        max_action = action
                colored_arrs[el][max_node] = True
                actions.append(max_node)
                q_pred.append(max_action)

            else: # with probability of epsilon, random uncolored node is selected for coloring
                found = False
                while not found:
                    node = random.randint(0, node_cnt[el] - 1) # random node is selected until an uncolored node is found
                    if not colored_arrs[el][node]:
                        found = True
                        colored_arrs[el][node] = True
                        embeddings = np.concatenate([node_embeds[node], graph_embeds]) # final embedding forthe selected node is created
                        embeddings = torch.from_numpy(embeddings).float()
                        with torch.no_grad():
                            action_val = self.local_qnet(embeddings) # action value for the node is calculated
                        q_pred.append(action_val)
                        actions.append(node)

        return actions, torch.Tensor(q_pred).requires_grad_(), not_finished
    
    def get_rewards(self, batch, colors, max_colors):
        # rewards are calculated for each graph in batch
        rewards = [0]*batch
        for el in range(batch):
            if(colors[el] == -1):
                # if a graph is completely colored already, then the color is returned from 
                # C++ function as -1. In this case, there will be no reward. Reward is set to an 
                # absurd value for eliminating in later steps
                rewards[el] = -9999
            else:
                # if maximum color number used in this step is increased for the selected graph, then
                # the increase amount is set as negative reward
                rewards[el] = - max(0, - max_colors[el] + colors[el])
                if(max_colors[el] < colors[el]):
                    # maximum color used for the selected graph is updated
                    max_colors[el] = colors[el]
        return np.array(rewards)

    def get_loss(self, graphs, batch, rewards, actions):
        losses = []
        for el in range(batch):
            # for each graph, embeddings are retrieved
            node_embeds = graphs.get_node_embed(el)
            graph_embeds = graphs.get_graph_embed(el)
            # total embedding is constructed
            embeddings = np.concatenate([node_embeds[actions[el]], graph_embeds])
            embeddings = torch.from_numpy(embeddings).float()
            if(rewards[el] < -3):
                # if rewards is smaller than -3, that means that there is an absurd reward value,
                # therefore for the selected graph, no loss will be added
                continue
            with torch.no_grad():
                # loss is appended as reward + gamma * target network's prediction
                losses.append(rewards[el] + self.gamma * self.target_qnet(embeddings))
        return torch.Tensor(losses).requires_grad_()
