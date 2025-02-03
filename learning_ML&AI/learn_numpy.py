import numpy as np

# CONVERT
nump_array = np.array([[1,2,3],[4,5,6]])
# print(type(nump_array))

# CREATE
# (sub-arrays, rows, columns ) == shapes
data = np.random.rand(2,3,4) 
data_zeros = np.zeros((2,2,2))

# (sub-arrays, rows, columns), value that will fills
data_fills = np.full((2,3,4), 7)
data_ones = np.ones((2,2,2))
print(data)

# READ
data_shape = data.shape
data_dtype = data.dtype
data_size = data.size
# print(data_size)

# SLICING
arr = data[0]
slice_arr = data[0][0:2]
reverse_arr = data[-1]
single_arr_val = data[0][0][0]
# print(single_arr_val)

#UPDATE
# (5) is equal to five value
array1 = np.random.rand(5)
array2 = np.random.rand(5)
# print(array1)
# print(array2)

# BASIC MATH
add = np.add(array1, array2)
sub = np.subtract(array1, array2)
mult = np.multiply(array1, array2)
div = np.divide(array1, array2)
dot = np.dot(array1, array2)

# print("Addition", add)
# print("Subtraction", sub)
# print("Multiplication", mult)
# print("Division", div)
# print("Dot", dot)

# STATISTICAL FUNCTIONS
sqrt = np.sqrt(25)
ab = np.abs(-2)
power = np.power(2, 3)
log = np.log(25)
exp = np.exp([2,3])
mins = np.min(array1)
maxs = np.max(array1)

# print("SQRT VALUE", sqrt)
# print("ABSOLUTE VALUE", ab)
# print("POWER", power)
# print("LOG", log)
# print("EXPENENTIAL", exp)
# print("MINIMUMS", mins)
# print("MAXIMUMS", maxs)

# UPDATING THE SHAPE VALUE
# (-1) means any shape value default "6"
data_reshape = data.reshape((2,2,-1))
# print(data_reshape.shape)

# APPEND OR INSERT NEW VALUES
# zeroes = np.zeros((9))
# print(zeroes)
# # add value to the end
# zeroes = np.append(zeroes, [8, 9])
# print(zeroes)

# # Insert the value in the position you want
# # (array, index position, value)
# zeroes = np.insert(zeroes, 2, 89)
# print(zeroes)

# DELETE
# (numpy_array, level of array you want to delete, specifying it that you want to delete a row and not a column)
delete_np_arr = np.delete(data, 1, axis=1,)
# print("DELETED:", delete_np_arr)

np.save("new array", data)

# LOAD THE NP-ARRAY
np_arr = np.load("new array.npy")
print(np_arr)