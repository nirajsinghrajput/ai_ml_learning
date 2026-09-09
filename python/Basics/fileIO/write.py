f = open("demo.txt","w")        # w overwrite in a existing file
                                # if the given file doesn't exist it creates a new file
# f = open("demo.txt","a")      # a it append new data without overwritting

f.write("I am very pro at procastination")

f.close()