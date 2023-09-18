import pickle

# Load data from a .pkl file
with open('best_model.pkl', 'rb') as file:
    data = pickle.load(file)

print(data)
