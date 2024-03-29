# model test MCST vs random 

import random
import json
from app.state import *
from move_MCST import *

def main():
    num_of_data = int(input("Số bộ data: "))
    # Tên file viết tiếp vào
    FILENAME = 'traindata/data01.json'
    with open(FILENAME,'w') as file:
        train_data = {
            "train_details": []
        }
        json.dump(train_data, file)
    # Opening Move Data (0-10 moves)
    FILENAME_OPENING = 'traindata/opening.json'
    with open(FILENAME_OPENING,'w') as file:
        train_data = {
            "train_details": []
        }
        json.dump(train_data, file)

    # Middle Move Data (10-30 moves)
    FILENAME_MIDDLE = 'traindata/middle.json'
    with open(FILENAME_MIDDLE,'w') as file:
        train_data = {
            "train_details": []
        }
        json.dump(train_data, file)

    # Middle Move Data (30-50 moves)
    FILENAME_LATE = 'traindata/late.json'
    with open(FILENAME_LATE,'w') as file:
        train_data = {
            "train_details": []
        }
        json.dump(train_data, file)

    # Struggle Move Data (Khi số quân cờ đối thủ hơn phe mình)
    FILENAME_STRUGGLE = 'traindata/struggle.json'
    with open(FILENAME_STRUGGLE,'w') as file:
        train_data = {
            "train_details": []
        }
        json.dump(train_data, file)

    # Close Out Move Data (Khi số quân cờ đối thủ hơn phe mình)
    FILENAME_CLOSEOUT = 'traindata/closeout.json'
    with open(FILENAME_CLOSEOUT,'w') as file:
        train_data = {
            "train_details": []
        }
        json.dump(train_data, file)
    
    for i in range(num_of_data):
        # Opening Move Data (0-10 moves)
        FILENAME_OPENING_TEMP = 'traindata/opening_temp.json'
        with open(FILENAME_OPENING_TEMP,'w') as file:
            train_data = {
                "train_details": []
            }
            json.dump(train_data, file)

        # Middle Move Data (10-30 moves)
        FILENAME_MIDDLE_TEMP = 'traindata/middle_temp.json'
        with open(FILENAME_MIDDLE_TEMP,'w') as file:
            train_data = {
                "train_details": []
            }
            json.dump(train_data, file)

        # Middle Move Data (30-50 moves)
        FILENAME_LATE_TEMP = 'traindata/late_temp.json'
        with open(FILENAME_LATE_TEMP,'w') as file:
            train_data = {
                "train_details": []
            }
            json.dump(train_data, file)

        # Struggle Move Data (Khi số quân cờ đối thủ hơn phe mình)
        FILENAME_STRUGGLE_TEMP = 'traindata/struggle_temp.json'
        with open(FILENAME_STRUGGLE_TEMP,'w') as file:
            train_data = {
                "train_details": []
            }
            json.dump(train_data, file)

        # Close Out Move Data (Khi số quân cờ đối thủ hơn phe mình)
        FILENAME_CLOSEOUT_TEMP = 'traindata/closeout_temp.json'
        with open(FILENAME_CLOSEOUT_TEMP,'w') as file:
            train_data = {
                "train_details": []
            }
            json.dump(train_data, file)
        # Khởi tạo bàn cờ đầu tiên
        start_board = [[1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 1],
                        [1, 0, 0, 0, -1],
                        [-1, 0, 0, 0, -1],
                        [-1, -1, -1, -1, -1]]
        master_board = State(None, start_board)

        # Chọn MCST là 'X' (-1) hoặc 'O' (1)
        side_list = [1, -1]
        side = random.choice(side_list)
        # Chọn bên đi trước  
        turn = random.choice(side_list)
        # Nhập stt train
        # train_stt = input("Lần train thứ: ")

        remain_time = {
            "remain_time_x": 20000,
            "remain_time_o": 20000
        }
        
        remain_move = {
            "remain_move_x": 50,
            "remain_move_o": 50
        }

        outOfMove = False

        while True:
            #MCST Turn
            if turn == side:
                # Hiện tại đang gọi hàm move, sẽ thay bằng hàm train MCST sau khi define xong
                moveTuple = move(master_board.prev_board, master_board.board, turn, remain_time["remain_time_x"], remain_time["remain_time_o"])
                # Create Data
                new_data = {
                    "player": side,
                    "board": master_board.board,
                    "moveTuple": moveTuple
                }

                if turn == 1:
                    if remain_move["remain_move_o"] >= 40:
                        appendData(FILENAME_OPENING_TEMP, new_data)
                    elif remain_move["remain_move_o"] >= 20:
                        appendData(FILENAME_MIDDLE_TEMP, new_data)
                    else:
                        appendData(FILENAME_LATE_TEMP, new_data)
                else:
                    if remain_move["remain_move_x"] >= 40:
                        appendData(FILENAME_OPENING_TEMP, new_data)
                    elif remain_move["remain_move_x"] >= 20:
                        appendData(FILENAME_MIDDLE_TEMP, new_data)
                    else:
                        appendData(FILENAME_LATE_TEMP, new_data)

                if master_board.advantageTeam() != 0 and master_board.advantageTeam() != side:
                    appendData(FILENAME_STRUGGLE_TEMP, new_data)

                (O, X) = master_board.countPieceByTeam()
                if side == 1 and O >= int(0.75*16):
                    appendData(FILENAME_CLOSEOUT_TEMP, new_data)
                elif side == -1 and X >= int(0.75*16):
                    appendData(FILENAME_CLOSEOUT_TEMP, new_data)

                

            #Random Turn
            else:
                # Lấy list các quân cờ thuộc phe Random
                validPiece = []
                for item in master_board.pieceList:
                    if item.team == turn and len(item.posibleMove) > 0:
                        validPiece.append(item)
                piece = random.choice(validPiece)
                # Random move in validPiece
                moveTuple = random.choice(piece.posibleMove)

            print(moveTuple)
            master_board.boardMove(moveTuple)

            #Giảm remain_move
            if turn == 1:
                remain_move["remain_move_o"] -= 1
            else:
                remain_move["remain_move_x"] -= 1

            # Viết file txt kết quả:
            nowBoard = master_board.board
            writeStateFile("test/eve.txt", nowBoard)
            # Kiểm tra thắng cuộc
            if master_board.victor:
                # win_side = "MCST" if turn == side else "Random"
                win_side = ""
                if turn == side:
                    win_side = "MCST"
                    mergeData(FILENAME_OPENING, FILENAME_OPENING_TEMP)
                    mergeData(FILENAME_MIDDLE, FILENAME_MIDDLE_TEMP)
                    mergeData(FILENAME_LATE, FILENAME_LATE_TEMP)
                    mergeData(FILENAME_STRUGGLE, FILENAME_STRUGGLE_TEMP)
                    mergeData(FILENAME_CLOSEOUT, FILENAME_CLOSEOUT_TEMP)
                else:
                    win_side = "Random"
                print("End of game, the victory is " + str(win_side))

                printState(nowBoard)
                break
            if remain_move["remain_move_x"] == 0:
                print("End of game, player X is out of moves!")
                outOfMove = True

            elif remain_move["remain_move_o"] == 0:
                print("End of game, player O is out of moves!")
                outOfMove = True
                
            if outOfMove:
                if master_board.advantageTeam() == 0:
                    print("Hòa!!!")
                elif master_board.advantageTeam() == side:
                    print("End of game, the victory is MCST!")
                    mergeData(FILENAME_OPENING, FILENAME_OPENING_TEMP)
                    mergeData(FILENAME_MIDDLE, FILENAME_MIDDLE_TEMP)
                    mergeData(FILENAME_LATE, FILENAME_LATE_TEMP)
                    mergeData(FILENAME_STRUGGLE, FILENAME_STRUGGLE_TEMP)
                    mergeData(FILENAME_CLOSEOUT, FILENAME_CLOSEOUT_TEMP)
                else:
                    print("End of game, the victory is Random!")
                break

            print(remain_move)
            printState(nowBoard)

            turn *= -1 

def appendData(filename, newData):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["train_details"].append(newData)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file)

def mergeData(filename, filenameTemp):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        with open(filenameTemp, 'r') as file1:
            file1_data = json.load(file1)
            for ele in file1_data["train_details"]:
                file_data["train_details"].append(ele)
        file.seek(0)
        json.dump(file_data, file)


if __name__ == "__main__":
    main()