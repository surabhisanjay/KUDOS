CODE

import pygame,os,csv
from functools import partial
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/users/krish/appdata/local/programs/python/python310/lib/site-packages/tesseract'
pygame.init()
# MENU SCREEN
def MENU():
    def insert_image():
        def biggestContour(contours):
            biggest = np.array([])
            max_area = 0
            for i in contours:
                area = cv2.contourArea(i)
                if area > 50:
                    peri = cv2.arcLength(i, True)
                    approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                    if area > max_area and len(approx) == 4:
                        biggest = approx
                        max_area = area
            return biggest, max_area
        def reorder(mypts):
            mypts = mypts.reshape((4, 2))
            mypts_New = np.zeros((4, 1, 2), dtype=np.int32)
            add = mypts.sum(1)
            mypts_New[0] = mypts[np.argmin(add)]
            mypts_New[3] = mypts[np.argmax(add)]
            diff = np.diff(mypts, axis=1)
            mypts_New[1] = mypts[np.argmin(diff)]
            mypts_New[2] = mypts[np.argmax(diff)]
            return mypts_New
        def splitBoxes(img):
            rows = np.vsplit(img, 9)
            boxes = []
            for r in rows:
                cols = np.hsplit(r, 9)
                for box in cols:
                    boxes.append(box)
            return boxes
        def return_numbers(path):
            # Now we will read the image in our program
            # you have to put your image path in place of photo.jpg
            # Window name in which image is displayed
            window_name = 'Image'
            src=cv2.imread(path)
            # Using cv2.cvtColor() method
            # Using cv2.COLOR_BGR2GRAY color space
            # conversion code
            img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("image 0", img)
            img_blur = cv2.GaussianBlur(img, (5, 5), 1)  # adding Guassian Blur
            # cv2.imshow("image 0", img_blur)
            img_threshold = cv2.adaptiveThreshold(img_blur, 255, 1, 1, 11, 2)
            # cv2.imshow("image 1",img_threshold)


            # Displaying the image
            img_blank = np.zeros((450, 450, 0), np.uint8)


            # Find contour
            imgcontour = img.copy()
            imgBigcontour = img.copy()
            contours, hierarchy = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(imgcontour, contours, -1, (0, 255, 0), 3)  # draw all detected contours


            # Find the biggest contour and use it as sudoku
            biggest, maxArea = biggestContour(contours)


            if biggest.size != 0:
                biggest = reorder(biggest)
                cv2.drawContours(imgBigcontour, biggest, -1, (0, 0, 255), 25)
                pts1 = np.float32(biggest)  # prepare points for warp
                pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450, 450]])
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                imgWarpColored = cv2.warpPerspective(img, matrix, (450, 450))
                imgDetectedDigits = img_blank.copy()


            numbers = []
            imgSolvedDigits = img_blank.copy()
            boxes = splitBoxes(imgWarpColored)
            
            for i in range(len(boxes)):
                img = cv2.imwrite("C:/Users/krish/OneDrive/Pictures/KUDOSEDITED/box{}.jpeg".format(i), boxes[i])
                img_box = cv2.imread("C:/Users/krish/OneDrive/Pictures/KUDOSEDITED/box{}.jpeg".format(i))


                img_BGR = cv2.cvtColor(img_box, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2GRAY)
                sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
                thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                thresh = cv2.normalize(thresh, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
                res, thresh = cv2.threshold(thresh, 64, 255, cv2.THRESH_BINARY)


                # Fill everything that is the same colour (black) as top-left corner with white
                cv2.floodFill(thresh, None, (0, 0), 255)


                # Fill everything that is the same colour (white) as top-left corner with black
                cv2.floodFill(thresh, None, (0, 0), 0)


                #data = pytesseract.image_to_string(thresh, config='digits')
                #data = pytesseract.image_to_string(thresh, lang='eng', \
                                                   #config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
                data = pytesseract.image_to_string(thresh, lang='eng', \
                                           config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
                numbers.append(data)
                path = "C:/Users/krish/OneDrive/Pictures/KUDOSEDITED/box{}.jpeg".format(i)
                
                os.remove(path)


            print(numbers)
            final_num = []
            for i in numbers:
                if i != "":
                    final_num.append(int(i[0]))
                else:
                    final_num.append(0)


            l = [8, 17, 26, 35, 44, 53, 62, 71, 80, 89]
            final_num[26] = 0
            final_num[78] = 0
            final_num[68] = 9
            final_num[62] = 0
            for i in range(len(final_num)):
                if i in l and i != 0:
                    print(final_num[i], end="\n")
                else:
                    print(final_num[i], end=", ")
            final=[]
            for i in range(len(l)):
                row = []
                if i != 0:
                    for j in range(l[i - 1] + 1, l[i]):
                        row.append(final_num[j])
                else:
                    for j in range(l[i]):
                        row.append(final_num[j])
                final.append(row)
            return final_num


        # Create an instance of tkinter frame
        win = Tk()


        # Set the geometry of tkinter frame
        win.geometry("700x350")
        w=[]
        def open_file():
            file = filedialog.askopenfile(mode='r', filetypes=[('Image Files', '*.png')])
            if file:
                filepath = os.path.abspath(file.name)
                w.append(filepath)
                Label(win, text="The File is located at : " + str(filepath), font=('Aerial 40')).pack()


        # Add a Label widget
        label = Label(win, text="Please insert your sudoku image", font=('Georgia 50'))
        label.pack(pady=10)


        # Create a Button
        ttk.Button(win, text="Browse", command=open_file).pack(pady=20)
        win.mainloop()
        print(w)
        final_num = return_numbers(w[0])
        l = [8, 18, 27, 36, 45, 54, 63, 72]
        final = []
        for i in l:
            if i != 8:
                row = []
                for j in range(i, i + 9):
                    print(i)
                    row.append(final_num[j])
                final.append(row)
            else:
                row = []
                for j in range(0, 9):
                    row.append(final_num[j])
                final.append(row)
        print(final)
        playgame_screen(final)


    # SUDOKU GAME SCREEN
    def playgame_screen(grid_original):
        # User Input
        def insert(position):
            i, j = position[1], position[0]  # i-row-y coordn, j-column-x coordn
            running = True
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        # If User Tries Editing Orginal Grid Numbers(Question)
                        if (grid_original[i - 1][j - 1] != 0):
                            running = False
                        # If Input Number Is Valid(1-9) Then Edits Grid
                        if (0 < event.key - 48 < 10):
                            pygame.draw.rect(screen, screencolour,
                                             (position[0] * 50 + 5, position[1] * 50 + 5, 50 - 10, 50 - 10))
                            value = myfont.render(str(event.key - 48), True, enteredvaluecolour)
                            screen.blit(value, (position[0] * 50 + 15, position[1] * 50))
                            grid[i - 1][j - 1] = event.key - 48
                            pygame.display.update()
                            running = False
                        # If Input Number is 0- Clears Grid
                        if event.key - 48 == 0:
                            grid[i - 1][j - 1] = 0
                            pygame.draw.rect(screen, screencolour,
                                             (position[0] * 50 + 5, position[1] * 50 + 5, 50 - 10, 50 - 10))
                            pygame.display.update()
                            running = False
                        return


        # Sudoku Solution using Backtracking/Recursive Algorithm
        def solution():
            # Checks If Guess Is Valid
            def is_valid(guess, row, col):
                # Checking Row
                row_vals = grid_solution[row]
                if guess in row_vals:
                    return False
                # Checking Column
                col_vals = []
                for i in range(9):
                    col_vals.append(grid_solution[i][col])
                if guess in col_vals:
                    return False
                # Checking 3*3 Grid
                grid_vals = []
                row_start = (row // 3) * 3
                col_start = (col // 3) * 3
                for i in range(row_start, row_start + 3):
                    for j in range(col_start, col_start + 3):
                        grid_vals.append(grid_solution[i][j])
                if guess in grid_vals:
                    return False
                # If Valid
                return True


            # Main Algorithm
            def solve_sudoku(row, col):
                # When at Last Box in Grid
                if row == 8 and col == 9:
                    return True
                # When at Last Column in Row
                if col == 9:
                    row += 1
                    col = 0
                # If Number>0 Exists In Box Of Solution Grid
                if grid_solution[row][col] > 0:
                    return solve_sudoku(row, col + 1)
                # Making Guess (1-9)
                for guess in range(1, 10):
                    # If Guess Is Valid->Adds Guess To Solution
                    if is_valid(guess, row, col):
                        grid_solution[row][col] = guess
                        if solve_sudoku(row, col + 1):
                            return True
                    # If Guess Not Valid
                    grid_solution[row][col] = 0
                return False


            if solve_sudoku(0, 0):
                return
            else:
                print("no solution exists")


        # Function To Draw "Sudoku Grid With Answers"
        def rightanswerboard(screen):
            # To Draw 9*9Grid
            for i in range(10):
                # To Make Bold Lines
                if i % 3 == 0:
                    pygame.draw.line(screen, (0, 0, 0), (50 * i + 50, 50), (50 * i + 50, 500), 4)
                    pygame.draw.line(screen, (0, 0, 0), (50, 50 * i + 50), (500, 50 * i + 50), 4)
                # To Make Normal Lines
                else:
                    pygame.draw.line(screen, (0, 0, 0), (50 * i + 50, 50), (50 * i + 50, 500), 2)
                    pygame.draw.line(screen, (0, 0, 0), (50, 50 * i + 50), (500, 50 * i + 50), 2)
            # Entering Values From Original Grid
            for i in range(len(grid_original)):  # row: y coordn
                for j in range(len(grid_original[0])):  # column: x coordn
                    if 0 < grid_original[i][j] < 10:
                        value = myfont.render(str(grid_original[i][j]), True, originalvaluecolour)
                        screen.blit(value, (j * 50 + 50 + 15, i * 50 + 50 + 3))
            solution()
            # Adding Solved Numbers From Solution Grid
            for i in range(9):
                for j in range(9):
                    if grid_original[i][j] == 0:
                        value = myfont.render(str(grid_solution[i][j]), True, enteredvaluecolour)
                        screen.blit(value, (j * 50 + 50 + 15, i * 50 + 50 + 3))
            pygame.display.update()


        # ANSWER SCREEN(After Answer button is clicked)
        def answersudoku():
            # Creating Answer Screen
            ans_screen = pygame.display.set_mode(screendimensions)
            sudokubackground = pygame.image.load('C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\rays.jpg')
            ans_screen.blit(sudokubackground, (0, 0))
            pygame.display.set_caption("KUDOS-SUDOKU-ANSWER")
            pygame.display.set_icon(icon)
            rightanswerboard(ans_screen)
            message = messagefont.render("CORRECT ANSWER ABOVE", True, (0, 0, 0))
            ans_screen.blit(message, (150, 525))
            # Drawing Menu Button
            pygame.draw.rect(screen, (0, 0, 0), (300, 575, 200, 50))
            menubutton = myfont.render("MENU", True, white)
            ans_screen.blit(menubutton, (350, 575))
            pygame.display.update()
            # Overall User Activity In Answer Screen
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        # MENU BUTTON
                        if 300 <= pos[0] <= 500 and 575 <= pos[1] <= 625:
                            MENU()
                            running = False
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            running = False


        # RESULT SCREEN(After Submit Button is clicked)
        def checksudoku():
            # Creating Result Screen
            result_screen = pygame.display.set_mode(screendimensions)
            sudokubackground = pygame.image.load(r'C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\rays.jpg')
            result_screen.blit(sudokubackground, (0, 0))
            pygame.display.set_caption("KUDOS-SUDOKU-YOUR RESULT")
            pygame.display.set_icon(icon)
            # Adding Answer Grid To Screen
            rightanswerboard(result_screen)


            # To Check If Sudoku Solved Correctly
            def solved_correctly():
                solution()
                for i in range(9):
                    for j in range(9):
                        if grid_solution[i][j] != grid[i][j]:
                            return False
                return True


            if solved_correctly():
                message = messagefont.render("KUDOS,YOU SUCCESSFULLY COMPLETED IT!", True, (0, 0, 0))
                result_screen.blit(message, (50, 550))
            else:
                message = messagefont.render("OOPS, INCORRECT ANSWER!", True, (0, 0, 0))
                result_screen.blit(message, (150, 550))
                message = messagefont.render("RIGHT ANSWER DISPLAYED ABOVE", True, (0, 0, 0))
                result_screen.blit(message, (100, 570))
            # Drawing Menu Button
            pygame.draw.rect(screen, (0, 0, 0), (300, 600, 200, 45))
            menubutton = myfont.render("MENU", True, white)
            result_screen.blit(menubutton, (350, 600))
            pygame.display.update()
            # Overall User Activity In Result Screen
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        # MENU BUTTON
                        if 300 <= pos[0] <= 500 and 600 <= pos[1] <= 650:
                            MENU()
                            running = False
                        if event.type == pygame.QUIT:  # to quit/close the board
                            pygame.quit()
                            running = False


        # __Variables____
        screendimensions = (550, 650)
        screencolour = (224, 224, 224)
        originalvaluecolour = (52, 31, 151)
        enteredvaluecolour = (0, 0, 0)
        white = (255, 255, 255)
        myfont = pygame.font.SysFont("Comic Sans", 35)
        messagefont = pygame.font.SysFont("Comic Sans", 20)
        grid = [[j for j in i] for i in grid_original]
        grid_solution = [[j for j in i] for i in grid_original]
        # Creating Sudoku Game Screen
        screen = pygame.display.set_mode(screendimensions)
        sudokubackground = pygame.image.load(r'C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\rays.jpg')
        screen.blit(sudokubackground, (0, 0))
        pygame.display.set_caption("KUDOS-A SUDOKU GAME")
        icon = pygame.image.load(r"C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\rubik.png")
        pygame.display.set_icon(icon)
        # Drawing Buttons- Submit and Answer
        pygame.draw.rect(screen, (0, 0, 0), (50, 550, 200, 50))
        pygame.draw.rect(screen, (0, 0, 0), (300, 550, 200, 50))
        submitbutton = myfont.render("SUBMIT", True, white)
        screen.blit(submitbutton, (50 + 20, 550))
        answerbutton = myfont.render("ANSWER", True, white)
        screen.blit(answerbutton, (300 + 20, 550))
        # Drawing 9*9 Grid(lines)
        for i in range(10):
            # Bold Lines
            if i % 3 == 0:
                pygame.draw.line(screen, (0, 0, 0), (50 * i + 50, 50), (50 * i + 50, 500), 4)
                pygame.draw.line(screen, (0, 0, 0), (50, 50 * i + 50), (500, 50 * i + 50), 4)
            # Normal Lines
            else:
                pygame.draw.line(screen, (0, 0, 0), (50 * i + 50, 50), (50 * i + 50, 500), 2)
                pygame.draw.line(screen, (0, 0, 0), (50, 50 * i + 50), (500, 50 * i + 50), 2)
        # Entering Values To Grid
        for i in range(len(grid_original)):  # row:y coordn
            for j in range(len(grid_original[0])):  # column:x coordn
                if 0 < grid_original[i][j] < 10:
                    value = myfont.render(str(grid_original[i][j]), True, originalvaluecolour)
                    screen.blit(value, (j * 50 + 50 + 15, i * 50 + 50 + 3))
        # Checking overall user activity in play game screen
        running = True
        while running:
            pygame.display.update()  # update all changes in screen
            for event in pygame.event.get():  # gets all events in board
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if 300 < pos[0] < 500 and 550 < pos[1] < 600:  # answer button
                        answersudoku()
                        break
                    elif 50 < pos[0] < 250 and 550 < pos[1] < 600:  # submit button
                        checksudoku()
                        break
                    else:  # anywhere else
                        insert((pos[0] // 50, pos[1] // 50))
                if event.type == pygame.QUIT:  # to quit/close the board
                    running = False


    
    pygame.init()
    # Creating Menu Screen
    menu_screen = pygame.display.set_mode((800, 450))
    pygame.display.set_caption("KUDOS-A SUDOKU GAME-MENU")
    icon = pygame.image.load(r"C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\rubik.png")
    pygame.display.set_icon(icon)
    background = pygame.image.load(r'C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\2.png')
    menu_screen.blit(background, (0, 0))
    # Checks Overall User Activity In Menu Screen
    running = True
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                # PLAY GAME BUTTON
                if 144 < pos[0] < 340 and 220 < pos[1] < 360:
                    grid_original = grid_original = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                                                     [5, 2, 0, 0, 0, 0, 0, 0, 0],
                                                     [0, 8, 7, 0, 0, 0, 0, 3, 1],
                                                     [0, 0, 3, 0, 1, 0, 0, 8, 0],
                                                     [9, 0, 0, 8, 6, 3, 0, 0, 5],
                                                     [0, 5, 0, 0, 9, 0, 6, 0, 0],
                                                     [1, 3, 0, 0, 0, 0, 2, 5, 0],
                                                     [0, 0, 0, 0, 0, 0, 0, 7, 4],
                                                     [0, 0, 5, 2, 0, 6, 3, 0, 0]]
                    playgame_screen(grid_original)


                elif 446<pos[0]<640 and 222<pos[1]<356:
                    insert_image()
                break


# LOGIN WINDOW
def login():
    # After Login Button On Login Screen Is Clicked
    def validateLogin(username, password):
        name = username.get()
        passwd = password.get()
        # CSV File To Store Player Names And Passwords
        with open(r"C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\playersKUDOS.csv", "a+", newline='') as f1:
            write = csv.writer(f1)
            # If File Empty-> add info to file
            if os.stat(r"C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\playersKUDOS.csv").st_size == 0:
                print("file empty:", os.stat(r"C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\playersKUDOS.csv").st_size == 0)
                write.writerow((name, passwd))
                print("Written on file:", (name, passwd))
            # If File Not Empty
            else:
                f1.seek(0,0)
                read = csv.reader(f1,delimiter=",")
                print("FILE:",read)
                for t in read:
                    print("TUPLE AT:",t)
                    # If Username Exists
                    if name == t[0]:
                        found=True
                        # If Password Doesn't Match-> moves back to main_screen
                        if passwd != t[1]:
                            print("Username found: password doesn't match")
                            loginwindow.destroy()
                            main()
                            # If Password Matches-> moves to menu_screen
                        if passwd == t[1]:
                            print("Username found, password matches")
                            break
                    # If Username Doesn't Exist-> add info to file
                    else:
                        found=False
                if found==False:
                    print("Username not found")
                    write.writerow((name,passwd))
        loginwindow.destroy()
        MENU()
    # To Close Main Screen
    pygame.quit()
    # To Create Login Screen using Tkinter
    # Window
    loginwindow = Tk()
    loginwindow.geometry("400x150")
    loginwindow.title("LOGIN FORM- KUDOS")
    # Username Label and Username Entry Box
    usernameLabel = Label(loginwindow, text="User Name").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(loginwindow, textvariable=username).grid(row=0, column=1)
    # Password Label and Password Entry Box
    passwordLabel = Label(loginwindow, text="Password").grid(row=1, column=0)
    password = StringVar()
    passwordEntry = Entry(loginwindow, textvariable=password).grid(row=1, column=1)
    validateLogin = partial(validateLogin, username, password)
    # Login button
    loginButton = Button(loginwindow, text="Login", command=validateLogin).grid(row=4, column=0)
    loginwindow.mainloop()


# MAIN SCREEN
def main():
    pygame.init()
    # Creating Main Screen
    main_screen = pygame.display.set_mode((800, 450))
    pygame.display.set_caption("KUDOS-A SUDOKU GAME")
    icon = pygame.image.load(r"C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\rubik.png")
    pygame.display.set_icon(icon)
    background = pygame.image.load(r"C:\Users\krish\OneDrive\Pictures\KUDOSEDITED\1.png")
    main_screen.blit(background, (0, 0))
    # Checking User Activity In Main Screen
    running = True
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            # If User Clicks On Main Screen
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                # If Login Button Clicked
                if 264 <= pos[0] <= 496 and 246 <= pos[1] <= 314:
                    login()
                    running = False
            # If Main Screen Is Closed
            if event.type == pygame.QUIT:
                running = False


#Calling Main Screen
main()





