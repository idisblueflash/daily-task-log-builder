from services import FlashLogReader

if __name__ == '__main__':
    reader = FlashLogReader()
    reader.parse()
    reader.report()
    reader.save_excel()
