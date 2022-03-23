from random import randint
from BoardClasses import Move
from BoardClasses import Board
from copy import deepcopy
import random
import random
from math import log, sqrt

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.




class MonteCarlo:

    def __init__(self, root_node):
        self.root_node = root_node
        self.child_finder = None
        self.node_evaluator = lambda child, montecarlo: None    

    def make_choice(self):
        best_children = []
        most_visits = float('-inf')
        print(len(self.root_node.children))
        for child in self.root_node.children:
	        if child.visits > most_visits:
		        most_visits = child.visits
		        best_children = [child]
	        elif child.visits == most_visits:
		        best_children.append(child)
        #print(best_children)
        return random.choice(best_children)

    
    def treepolicy(self, currentnode):
        """ Given root node, find the leaf node based on UCT"""
        cur_node = currentnode
        state = deepcopy(currentnode.state)
        
        while True:
            legal_moves = [move  for moves in cur_node.state.get_all_possible_moves(cur_node.color) for move in moves]
        
            if cur_node.state.is_win(cur_node.color) != 0:
                #print(cur_node.state.is_win(cur_node.color))
                ##ZZZ backpropagate
                return cur_node
                

            elif len(cur_node.children) < len(legal_moves):
                # Children are not fully expanded, expand one.
                unexpanded = [
                    move for move in legal_moves
                    if move not in cur_node.moves_expanded
                ]

                assert len(unexpanded) > 0
                move = random.choice(unexpanded)

                next_state = deepcopy(cur_node.state)

                next_state.make_move(move, cur_node.color)
          
                child = Node(next_state)
                child.move = move
                child.color = 2 if cur_node.color == 1 else 1
                cur_node.add_child(child)
                #print(len(cur_node.children), len(legal_moves))
                #print(child.depth)
                #self.state_node[next_state] = child
                return child

            else:
                # Every possible next state has been expanded, pick one.
                node = cur_node.get_preferred_child(self.root_node)
                if(node != None):
                    cur_node = node
                else:
                    return cur_node

        return cur_node
        
    def backpropagate(self, node, result):    
        while(node != None):
            node.visits += 1
            sign = 1 if self.root_node.color == node.color else -1
            node.win_value += sign * result
            node = node.parent
            
                
    def simulate(self, expansion_count = 1):
        
        for iters in range(expansion_count):
            #print("iterations:",iters)
            #select and expand
            picked_node = self.treepolicy(self.root_node)
            #print("depth:",picked_node.depth, picked_node.color)
            
            #rollout
            result = self.random_rollout(picked_node)
            #backpropagate
            self.backpropagate(picked_node, result)



    def random_rollout(self, node):
        #print("root_node:", self.root_node.color)
        board = deepcopy(node.state)
        color = node.color
        result = board.is_win(color)
        #print(node.color, node.depth)
        #print(result)
        while result == 0:
            moves = board.get_all_possible_moves(color)
            if len(moves) == 0:
                if color == 1:
                    return 0
                else:
                    return 1
                board.show_board(None)
                #return 0
            index = randint(0,len(moves)-1)
            inner_index =  randint(0,len(moves[index])-1)
            move = moves[index][inner_index] 
            board.make_move(move,color)
            color = 2 if color == 1 else 1
            result = board.is_win(color)
        #print(result)
        if result == -1:
            return 0.5
        elif result == self.root_node.color:
            return 1 
        else:
            return 0         

class Node:

    def __init__(self, state):
	    self.state = state
	    self.win_value = 0
	    self.policy_value = None
	    self.depth = 0
	    self.visits = 0
	    self.parent = None
	    self.children = []
	    self.fullexpanded = False
	    self.player_number = None
	    self.discovery_factor = 1.5
	    self.move = None
	    self.color = None
	    self.moves_expanded = set()

    def update_win_value(self, value):
	    self.win_value += value
	    self.visits += 1

	    if self.parent:
		    self.parent.update_win_value(value)

    def update_policy_value(self, value):
        self.policy_value = value

    def add_child(self, child):
        child.depth += self.depth  + 1
        self.children.append(child)
        child.parent = self

    def add_children(self, children):
        for child in children:
	        self.add_child(child)

    def get_preferred_child(self, root_node):
        best_children = []
        best_score = float('-inf')

        if len(self.children) == 0:
            print("number",self.children)
            self.state.show_board(None)
            return None
        for child in self.children:
	        score = child.get_score(root_node)

	        if score > best_score:
		        best_score = score
		        best_children = [child]
	        elif score == best_score:
		        best_children.append(child)

        return random.choice(best_children)

    def get_score(self, root_node):
        discovery_operand = self.discovery_factor  * sqrt(log(self.parent.visits) / max(self.visits, 1))
        win_operand = self.win_value / (max(self.visits ,1))

        self.score = win_operand + discovery_operand

        return self.score

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            print("color")
            self.color = 1
        """  
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]   
        """
        #print(self.color)
        move = self.mcts()
        print("mtcs")
        self.board.make_move(move,self.color)
        
        return move
        
    def mcts(self):
        node = Node(self.board)
        node.color = self.color
        #print(self.color)
        montecarlo = MonteCarlo(node)
        #montecarlo.child_finder = self.child_finder
        #montecarlo.node_evaluator = self.node_evaluator
        
        montecarlo.simulate(500)
        node = montecarlo.make_choice()
        move = node.move
        return move
       
    def child_finder(self, node, montecarlo):
        for moves in node.state.get_all_possible_moves(node.color):
            for move in moves:
                child = Node(deepcopy(node.state))
                child.state.make_move(move, node.color) 
                child.color = self.opponent[node.color]
                child.player_number = self.opponent[node.player_number]
                child.move = move
                node.add_child(child)
        return None  
    """
    def node_evaluator(self, node, montecarlo):
        win = node.state.is_win(node.color)
        #print(win)
        if win == -1:
            return 0.5
        elif win == 0:
            return None
        elif win == node.color:
            return 0.5
        return None"""
