""" 
COMP 614
Statistics
Jorgo Qirjaj 
"""

import math


def arithmetic_mean(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the arithmetic mean of the data set.
    """
    if len(data) == 0:
        return None					
    avg = sum(data) / len(data)		# Average formula, sum of data / number of data
    return avg

#print(arithmetic_mean([13, 11, 7, 5, 6]))


def pop_variance(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the population variance of the data set.
    """
    if len(data) == 0:
        return None
    
    avg = arithmetic_mean(data)		# Using first helper function to calc mean
    diff_list = []					# Empty list to hold the squared differences							
    for num in data:				# Loops through each value to compute squared diff
        diff = (num - avg)**2		
        diff_list.append(diff)		# Appends each value to the empty diff_list
        
    return arithmetic_mean(diff_list) # Variance is the mean of diff_list

#print(pop_variance([3, 7, 1, 2, 10]))


def std_deviation(data):
    """
    Given a list of numbers representing a data set, computes and returns 
    the standard deviation of the data set.
    """
    if len(data) == 0:
        return None
    
    std_dev = math.sqrt(pop_variance(data))	# Computes std deviation as the sqrt(variance)
    return std_dev

#print(std_deviation([3, 7, 1, 2, 10]))

def moving_avg(data, num_days):
    """
    Given a list of numbers representing a data set and an integer representing
    a number of days, builds and returns a new list where the i-th element is 
    the average of the data over the input number of days starting at position
    i in the data list.
    """
    # If number of days is more than values in data, return the avg(data)
    if num_days >= len(data):
        return [arithmetic_mean(data)] # Returns a list of 1 element, mean of input list
    
    # If number of days is more than values in data, return the avg(data)
    elif num_days <= 0: 
        return None
    
    # Empty list which will store the calculated moving average
    moving_avgs_list = []						
    
    # For every new sublist created, compute its average and add it to moving_avgs_list 
    for index in range(len(data) - num_days + 1): 		# Range of no of sublists created
        avg = arithmetic_mean(data[index : index + num_days]) 	# Finds average of sublist 
        moving_avgs_list.append(avg)						   	# Appends each avg to list
    return moving_avgs_list

#print(moving_avg([5, 2, 8, 3, 7, 4], 3))

def clean_with_deletion(data):
    """
    Given a list of lists representing a data set, cleans the data by creating
    and returning a new list of lists that contains the same data, minus any 
    rows that were originally missing values (denoted by None). Should not 
    mutate the original list.
    """
    clean_list = [data[0][:]] 			# Creates a new list, and copies the header row  
    for row in data[1:]:				# Looping through every row (skips header)
        if None not in row:				# Excludes rows with missing values
            clean_list.append(row[:])	# Then, adds a copy of that row to the new list
    return clean_list					

#print(clean_with_deletion([ 
# ["age (years)", "height (inches)"],
# [25, None],
# [40, 63],
# [81, None],
# [None, 69],
# [52, 74]]))


def column_avgs(data):
    """
    Given a list of lists representing a data set, returns a new list where the
    i-th element is the arithmetic mean of the i-th column in the data set.
    """
    # New list, will store mean of each col
    new_list = []								

    # Loop over each column index (based on header length)
    for col in range(len(data[0])): 	# In the range of number of columns
        data_values = []
     

        # Goes through each row, skips header row
        for row in data[1:]:
            if row[col] is not None:	# Excludes invalid values (i.e. None)
                data_values.append(row[col])
       

        # If there are no valid values in this column, append None
        if len(data_values) == 0:
            new_list.append(None)
        # Otherwise, append the avg of the data of that column
        else:
            new_list.append(arithmetic_mean(data_values))
    return new_list

#print(column_avgs([
# ["age (years)", "height (inches)"],
# [None, None],
# [40, 63],
# [81, None],
# [None, 69],
# [52, 74]]))

def clean_with_mean(data):
    """
    Given a list of lists representing a data set, cleans the data by creating
    and returning a new list of lists that contains the same data, but with
    any values that were originally missing (denoted by None) filled in with 
    the arithmetic mean of the corresponding column.
    """
    
    column_mean = column_avgs(data)	# Computes mean for each column 
    clean_list = [data[0][:]]		# Copy of header row	
    
    for row in data[1:]:			# Loops through each data row, skipping header
        new_row = []				# Creates a new row so the original data is not changed
        for col in range(len(row)):	# Loops through each column in that row
            if row[col] is None: 	# If the value is missing, substitute with mean of col
                new_row.append(column_mean[col])
            else:
                new_row.append(row[col]) # Otherwise, appends original row to new ds
        clean_list.append(new_row)	# Appends the copied row to the cleaned dataset

    return clean_list

#print(clean_with_mean([
# ["age (years)", "height (inches)"],
# [25, None],
# [40, 63],
# [81, None],
# [None, 69],
# [52, 74]]))
