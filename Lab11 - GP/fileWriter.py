class FileWriter:
    instance = None

    def __init__(self, path):
        self._file = open(path, 'w+')

    @staticmethod
    def getFileWriter():
        if FileWriter.instance is None:
            FileWriter.instance = FileWriter('output.txt')
        return FileWriter.instance

    def write(self, text):
        print(text)
        self._file.write(text + '\n')

    def __del__(self):
        self._file.flush()
        self._file.close()
