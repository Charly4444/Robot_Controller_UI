import re
from tcp_sendmsg import send_message_and_receive_response as tcpSENDMsg

"""
This Code is part of the RobotArm Controller v1.0 project the key function is
to recieve a boardArray[] and commandMsg and return an Updated boardArray[]
to the calling function if the command was successfull
«Polytech'24»
"""
def algorithmManager(boardArray, commandmsg):
    board = boardArray
    command = commandmsg

    #1 CHECK THE INSTRUCTION PARSED
    # ================================================================
    # Check format
    if not re.match(r'^Move,\d+,\d+$', command):
        raise ValueError("Invalid command format")
    
    # extract row and column from command
    parts = command.split(',')
    start_cell_number = int(parts[1])
    start_col = (start_cell_number - 1) % 8
    start_row = (start_cell_number - 1) // 8
    end_cell_number = int(parts[2])
    end_col = (end_cell_number - 1) % 8
    end_row = (end_cell_number - 1) // 8

    # ===================================================================


    
    #2 CHECK IF VALID MOVE (SPACE)
    # ===================================================================
    if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
        raise ValueError("Invalid coordinates")
    if board[start_row][start_col] != 1 or board[end_row][end_col] != 0:
        raise ValueError("Invalid move")

    # ===================================================================
    


    #3 GENERATE TCP COMMAND AND SEND IT !
    # ===================================================================
    parts = command.split(',')
    modified_parts = [parts[0]] + ['1,' + part for part in parts[1:]]  # Insert '1' before each part except the command itself
    fullcommand = ','.join(modified_parts)  #now like; Move,1,2,1,5 -> for example
    # # send the fullcommand
    response = tcpSENDMsg(fullcommand)
    
    # ===================================================================
    # hard set (for Test)
    # response = "Done\r\n"


    #4 CHECK RESPONSE AND UPDATE BOARD
    # ===================================================================
    if response == "Done\r\n":
        print("You Moved a Piece")
        # now call is successfull, update board
        print('updating the board!!!')
        board[start_row][start_col] = 0
        board[end_row][end_col] = 1

        print("Updated board:")
    else:
        print("An error occurred:", response)
    # ================================================
    # we can also see what board looks like on console
    for row in board:
        print(' '.join('x' if cell == 1 else 'o' for cell in row))
    # ================================================
    
    return board    #board array is returned
