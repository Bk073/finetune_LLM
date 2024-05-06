import re

def clean_text(text):
    cleaned_text = re.sub(r"[',\"]", '', text)
    return cleaned_text

def read_file(path_):
    # with open(path_, 'r', encoding='utf-8') as f:
    #     text = f.read()
    # return text
    cleaned_line = []
    with open(path_) as f:
        lines = f.readlines()
        for line in lines:
            words = line.split()
            if len(words) > 10:
                cleaned_line.append(line)
    return cleaned_line

def save_file(path_, text):
    with open(path_, 'w', encoding='utf-8') as f:
        f.write(" ".join( t for t in text))
        
if __name__ == '__main__':
    text = read_file('./cdc_b_cleaned.txt')
    # cleaned_text = clean_text(text)
    save_file('./cdc_b_cleaned_mar_19.txt', text)

