def generate_moves(arr1, arr2):
    # Check if the arrays have the same number of 1s and 0s
    count_1_arr1 = sum(row.count(1) for row in arr1)
    count_0_arr1 = sum(row.count(0) for row in arr1)
    count_1_arr2 = sum(row.count(1) for row in arr2)
    count_0_arr2 = sum(row.count(0) for row in arr2)
    
    if count_1_arr1 != count_1_arr2 or count_0_arr1 != count_0_arr2:
        print("Arrays don't have the same number of 1s and 0s.")
        return []
    
    passed = []
    moves = []

    # replacer
    def replacer(arr1, arr2, val):
        for k in reversed(range(8)):
            for l in reversed(range(8)):
                if (k,l) not in passed:
                    
                    if arr1[k][l] != arr2[k][l] and arr1[k][l] != val and (k,l) not in passed:
                        passed.append((k,l))
                        return ((k,l))
   

    # Iterate through the arrays and generate moves
    for i in range(8):
        for j in range(8):
            if (i,j) not in passed:

                if arr1[i][j] != arr2[i][j]:
                    # Iterate the array backward to find a replacement
                    val = arr1[i][j]

                    # Call to find replacement
                    (k,l) = replacer(arr1,arr2,val)
                    if(val==1):
                        moves.append(((i*8 + j + 1), (k*8 + l + 1)))
                    else:
                        moves.append(((k*8 + l + 1), (i*8 + j + 1)))
                    
                    passed.append((i,j))
                    # they're same
                else:
                    passed.append((i, j))
    return moves