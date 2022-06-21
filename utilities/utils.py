def writeToFile(path, content):
    f = open(path, 'w+')
    f.write(content)
    f.close()