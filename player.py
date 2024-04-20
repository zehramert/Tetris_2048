import os

class Player:

    difficulty = 0 # 0 represents easy, 1 represents normal, 2 represents hard
    high_score = 0
    volume = 50
    music_on = True
    save_list = []

    def __init__(self):
        # get the directory in which this python code file is placed
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # compute the path of the image file
        save_file_location = current_dir + "/save/save.save"
        # Import values from save file to list
        save_file = open(save_file_location, "r")
        self.save_list = save_file.readlines()
        save_file.close()
        # Importing difficulty
        if (int(self.save_list[0]) == 1):
            self.difficulty = 1
        elif (int(self.save_list[0]) == 2):
            self.difficulty = 2
        # Importing high score
        self.high_score = int(self.save_list[1])
        # Importing music volume
        self.volume = int(self.save_list[2])
        # Importing music on-off setting
        # 0 represents false, 1 represents True
        if (int(self.save_list[3]) == 0):
            self.music_on = False

    def getDiff(self):
        return self.difficulty

    def setDiff(self, number):
        self.difficulty = number

    def getHighScore(self):
        return self.high_score

    def setHighScore(self, number):
        self.high_score = number

    def getVolume(self):
        return self.volume

    def setVolume(self, number):
        if (number >= 0 and number <= 100):
            self.volume = number

    def turnMusicOn(self):
        self.music_on = True

    def turnMusicOff(self):
        self.music_on = False

    # Writes changed settings into the file
    def updateOnClose(self):
        # get the directory in which this python code file is placed
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # compute the path of the image file
        save_file_location = current_dir + "/save/save.save"
        # Import values to save file from Player object
        save_file = open(save_file_location, "w")
        save_file.write(str(self.difficulty) + "\n")
        save_file.write(str(self.high_score) + "\n")
        save_file.write(str(self.volume) + "\n")
        if (self.music_on):
            save_file.write("1")
        else:
            save_file.write("0")
        save_file.close()
