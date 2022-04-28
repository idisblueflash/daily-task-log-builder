from services import FlashDemoLogReader

if __name__ == '__main__':
    reader = FlashDemoLogReader()
    reader.parse()
    reader.report()
    reader.save_excel()
