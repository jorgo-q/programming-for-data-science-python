"""
Jorgo Qirjaj - COMP 614
Stock Prediction
"""

import comp614_module3 as stocks
import random


def markov_chain(data, order):
    """
    Creates and returns a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the Markov chain

    returns: a dictionary that represents the Markov chain
    """
    
    model = {} 
    for idx in range(len(data) - order): 		# Range from i to (m - n)
        state = tuple(data[idx : idx + order]) 	# Creates state w/ slice of order length
        next_value = data[idx + order]			# Identifies the next value is after this state
        

        if state not in model:					# Initialize state 
            model[state] = {}

        # .get returns the current count if the key exists, otherwise 0
        model[state][next_value] = model[state].get(next_value, 0) + 1 
        
    # This will conver the counts to probablities
    for state, trs in model.items(): 	# Loops through states and their transition counts
        total = sum(trs.values())
        for next_value in trs: 
            trs[next_value] /= total # Dividing to get probability
                
    return model

def predict(model, last, num):
    """
    Predicts the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    
    predictions = []
    current_state = list(last)			# Creates a copy to avoid mutation
    
    for _ in range(num): 
        state_tuple = tuple(current_state) 
        
        # Checks if the state exists in the model, and uses weighted rand choice
        if state_tuple in model: 
            trs = model[state_tuple]		# Gets next possible states & probabilities
            rand = random.random()			# Random no between 0 and 1
            cum = 0							# Calculates cumulative prob weights


            for next_val, prob in trs.items(): 
                cum += prob
                if rand <= cum:				# Picks value whose cum prob exceeds rand
                    pred = next_val
                    break
            else: 
                pred = next_val				# Fallback, if rounding leaves has no match
                    
    
    
        # Checks if state is not found, and picks rand int form 0-3 
        else: 
            pred = random.randrange(0, 4)
                    
        predictions.append(pred)			# Saves 1st predicted value
        current_state.pop(0) 				# Removes oldest element 
        current_state.append(pred)			# Then adds newly predicted value
        
        
    return predictions


def mse(result, expected):
    """
    Calculates the mean squared error between two data sets. Assumes that the 
    two data sets have the same length.
    
    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    total = 0
    for idx in range(len(result)):
        diff = result[idx] - expected[idx]	# Difference between predicted & actual
        total += diff**2					# Squares the diff and then adds it up
    return total / float(len(result))		

def run_experiment(train, order, test, future, actual, trials):
    """
    Runs an experiment to predict the future of the test data based on the
    given training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    new_model = markov_chain(train, order)	# Builds Markov model from training data 
    total_err = 0							
    
    for _ in range(trials): 				# Using _ since idx throws styling error if unused
        new_pred = predict(new_model, test, future)
        total_err += mse(new_pred, actual)

    avg_err = total_err / float(trials)		# Calculates average error for the no of trials
    return avg_err
    

def run():
    """
    Runs the stock prediction application.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Load the training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Load the test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()
        
run()
