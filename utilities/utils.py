path='E:\\Jana\\Github\\Python\\utilities\\'

def writeToFile(path, content):
    f = open(path, 'w+')
    f.write(content)
    f.close()