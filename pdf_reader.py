from PyPDF2 import PdfReader

def read(file_path):
    reader = PdfReader(file_path)
    text = ''
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = text + ' ' + page.extract_text()
    return text

def write_text(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("".join( t for t in text))

if __name__ == '__main__':
    file_path = './pregnancy/21.pdf'
    save_path = './pregnancy/21.txt'

    text = read(file_path)
    write_text(save_path, text)