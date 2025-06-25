# class Student():
#     def __init__(self,age,name):
#         self.info = {"name": name,"age": age,"grades": []}

#     def add_grade(self,grade):
#         self.info["grades"].append(grade)
        
#     def avg_grade(self):
#         result = sum(self.info["grades"]) // len(self.info["grades"])
#         print(result)

# student = Student(15, "Andrew")
# student.add_grade(12)
# student.add_grade(8)
# print(student.info["grades"][0])
# print(student.info["name"])
# print(student.info)
# student.avg_grade()


# class Playlist:
#     def __init__(self,song):
#         self.songs = []
#         self.songs.append(song)
#     def getFirstThree(self):
#         return self.songs[0][:3]
#     def getLastThree(self):
#         return self.songs[0][-3:]
#     def reversePlayList(self):
#         return self.songs[0][::-1]
#     def getEverySecond(self):
#         return self.songs[0][0::2]

# play = Playlist("Eminem")
# print(play.getFirstThree())
# print(play.getLastThree())
# print(play.reversePlayList())
# print(play.getEverySecond())


class Gamecharacter:
    def __init__(self,health,int,str,dex):
        self.stats = {"health": health,
                      "int": int,
                      "str": str,
                      "dex": dex
                      }
        
    def maxStats(self):
        return max(self.stats.values())
    
    def totalStats(self):
        return sum(self.stats.values())
    
    def normalizeStats(self):
        max2 = []
        for i in self.stats.values():
            if i >= 50:
                i = i - 50
                max2.append(i)
        self.normalize = min(max2) + 50
        print(self.normalize)
        return next(key for key,value in self.stats.items() if value == self.normalize)
        

player = Gamecharacter(100,20,70,10)
print(player.maxStats())
print(player.normalizeStats())
print(player.totalStats())
        