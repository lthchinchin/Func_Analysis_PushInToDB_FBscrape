from bs4 import BeautifulSoup
import urllib.request
import nltk
from nltk.tokenize import sent_tokenize
import re
import codecs
from underthesea import word_tokenize
import time
import pymysql
import os
import json
import datetime


def database(companyname, companymail, programinglanguage, jobposition, linkpost, descpost, status):
    try:
        db = pymysql.connect("localhost", "root", "", "fb_scrape_db")
        cursor = db.cursor()
        print("Kết nối với csdl thành công!")
    except:
        print("Không kết nối được với csdl!")

    sql = """
        INSERT INTO tbl_job_hirring (company_name,company_mail,programing_language,job_position,link_post,post_desc,status)
        VALUES
            (%s,%s,%s,%s,%s,%s,%s)
        """

    try:
        cursor.execute(sql, (companyname, companymail,
                             programinglanguage, jobposition, linkpost, descpost, status))
        db.commit()
        print("Lưu vào csdl thành công!")
    except:
        db.rollback()
        print("Lưu Thất bại!")
    db.close()


# database('sad', 'sad', 'asdsa',
#     'jobposition', 'link_post', 'text', 1)
# quit()
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


def func_TrainFor_checkSPAM():
    file_path = os.path.join(script_dir, "train_NLTK/checkwords_vn_train.txt")

    synonyms_raw = []
    synonyms = []
    while True:
        print("_Nhap vao tu muon train (press 0 de thoat): ")
        w = " ".join(re.sub(r"\W+|_", " ", input()).split())
        if(w == "0"):
            break
        synonyms_raw.append(w.lower())
    print("--Arr Input:"+str(synonyms_raw))

    # luot tu trung o khi nhap tu ban phim
    synonyms = list(set(synonyms_raw))
    synonyms_print = synonyms[:]
    f = codecs.open(
        file_path, "r", "utf8")
    keywords_for_check = f.read()
    f.close()
    ArrCheck = word_tokenize(keywords_for_check)

    # luot tu trung o trong file Train (lv2)
    print("synonyms : "+str(synonyms))
    print("synonyms_clone : "+str(synonyms_print))
    print("ArrCheck : "+str(ArrCheck))
    for i in synonyms:
        if(i == ''):
            synonyms_print.remove(i)
        for j in list(set(ArrCheck)):
            if(i.lower() == j.lower()):
                print("remove:"+i)
                synonyms_print.remove(i)

    print("--ArrSynonyms mang nay se duoc push vao file train: ")
    print(synonyms_print)

    f_a = codecs.open(
        file_path, "a", "utf8")
    if(len(synonyms_print) != 0):
        for i in synonyms_print:
            f_a.write(i+" ")
        f_a.write("\n")
        print("$Train Success!$")
    else:
        print("#Train Fail!")
    f_a.close()

    f_refresh = codecs.open(
        file_path, "r", "utf8")
    keywords_for_check = f_refresh.read()
    f_refresh.close()
    print("\n--In ra keywords_for_check(nhung gi co trong file train): ")
    # ArrCheck = keywords_for_check.split()
    ArrCheck = word_tokenize(keywords_for_check)
    print(ArrCheck)
# func_TrainFor_checkSPAM()


def func_TrainFor_programmingLanguage():
    file_path = os.path.join(script_dir, "train_NLTK/pl_train.txt")

    pl_raw = []
    while True:
        print("_Nhap ngon ngu lap trinh muon train (press 0 de thoat): ")
        # w = " ".join(re.sub(r"\W+|_", " ", input()).split())
        w = input().strip(" ")
        if(w == "0"):
            break
        pl_raw.append(w)
    t1 = time.time()
    print("--Arr Input:"+str(pl_raw))
    f = codecs.open(
        file_path, "r", "utf8")
    keywords_for_check = f.read()
    f.close()
    ArrCheck = keywords_for_check.split()
    pl_train = list(set(pl_raw))[:]
    for i in list(set(pl_raw)):
        for j in list(set(ArrCheck)):
            if i == "":
                pl_train.remove(i)
            if(i.lower() == j.lower()):
                pl_train.remove(i)
    print("--ArrPLTrain mang nay se duoc push vao file train: ")
    print(pl_train)
    f = codecs.open(
        file_path, "a", "utf8")
    if(len(pl_train) != 0):
        for i in pl_train:
            f.write(i+" ")
        f.write("\n")
        f.close()
        print("$Train programming languages Success!$")
    else:
        print("#Train Fail!")
    t2 = time.time()
    print("--processing time: "+str(t2-t1))
# func_TrainFor_programmingLanguage()


def func_pushcontent():
    file_path_file1 = os.path.join(script_dir, "file1.txt")
    file_path_file2 = os.path.join(script_dir, "file2.txt")

    f1 = codecs.open(file_path_file1, "r", "utf8")
    f2 = codecs.open(file_path_file2, "w", "utf8")
    arrtof2 = []  # mang nay day vao file 2
    content = f1.read().split()
    newcontent = []  # mang nay update file 1

    # lay data tu file 1 sang file 2
    print("_length content: "+str(len(content)))
    for i in content:
        arrtof2.append(i)
        if i == '},' or i == '}' or i == '}]':
            nodeDel = content.index(i)
            break
    for i in arrtof2:
        f2.write(i+" ")
    f2.write("\n")
    f2.close()
    #  cap nhat mang lai
    i = nodeDel+1
    while i < (len(content)):
        newcontent.append(content[i])
        i = i+1
    print("_update content: "+str(len(newcontent)))
    #  cap nhat file 1 lai
    f1a = codecs.open(file_path_file1, "w", "utf8")
    for i in newcontent:
        f1a.write(i+" ")
    f1a.close()
    f1.close()
# func_pushcontent()


def func_DataAnalysis():
    func_pushcontent()
    file_path_file2 = os.path.join(script_dir, "file2.txt")
    file_path_pl_train = os.path.join(script_dir, "train_NLTK/pl_train.txt")
    file_path_checkwords = os.path.join(
        script_dir, "train_NLTK/checkwords_vn_train.txt")
    file_path_stopwords = os.path.join(
        script_dir, "train_NLTK/vn_stopwords.txt")

    # content post raw and luot bo cac ki tu ngoai chu va so
    f = codecs.open(file_path_file2, "r", "utf8")
    text_raw = f.read()
    # bien cac ki tu dac biet thanh " "
    text = re.sub(r"\W+|_", " ", text_raw)
    # print("*Text raw: "+text_raw)
    # print("\nNoi Dung Chinh: ")
    tokens = word_tokenize(text)
    # print(text)
    # --
    # tim kiem ngon ngu lap trinh trong post
    programming_language = []
    company_email = re.findall(r'\S+@\S+', text_raw)
    # strip loai bo cac ki tu phia ngoai cung
    link_post = (
        (re.findall(r'(https?://www.facebook.com/[^\s]+)', text_raw))[0]).strip(',"')
    print("link_post: "+link_post)
    job_position_check = ["Senior", "Fresher",
                          "Intern", "Junior", "Tester", "Dev", "Software Test Intern", "Software Test Fresher"]
    company_syn = ["công ty", "cty"]
    job_position = []
    f = open(file_path_pl_train, "r")
    p_languges_raw = f.read()
    p_languges = p_languges_raw.split()
    # niceword = word_tokenize(analy1)
    for i in company_syn:
        for j in range(len(tokens)):
            if(i.lower() == tokens[j].lower()):
                company_name = tokens[j+1]
                break
            else:
                if company_email != None:
                    try:
                        company_name = (
                            ((company_email[0].split('.'))[0]).split('@'))[1]
                    except:
                        company_name = tokens[0]
                else:
                    company_name = tokens[0]
        if(i.lower() == tokens[j].lower()):
            break

    for i in tokens:
        for j in job_position_check:
            if(i.lower() == j.lower()):
                if(j not in job_position):
                    job_position.append(j)
    for i in text.split():
        for j in p_languges:
            if(i.lower() == j.lower()):
                if(j not in programming_language):
                    programming_language.append(j)

    print("--Company name: "+str(company_name))
    print("--Post nay nhac den cac nn lap trinh: "+str(programming_language))
    print("--Gmail company: "+str(company_email))
    print("--Link post: "+str(link_post))
    print("--Vi tri can tuyen: "+str(job_position))

    # print("--Desc: "+text)
    x = ''
    y = ''
    z = ''
    for i in programming_language:
        x = x+i+", "
    programminglanguage = x.strip(", ")
    for i in list(set(company_email)):
        y = y+i+", "
    companyemail = y.strip(", ")
    for i in job_position:
        z = z+i+", "
    jobposition = z.strip(", ")

    # --
    # print("ARR: "+str(tokens))  # day la noi dung file input da split

    # canh bao post co phai spam khong

    f = codecs.open(
        file_path_checkwords, "r", "utf8")
    text_check = f.read()
    Arr_check = word_tokenize(text_check)
    # print("ARR_check mang nay kiem tra day co phai post spam k ?: "+str(Arr_check))
    alert = 1
    for i in tokens:
        for j in Arr_check:
            if(i.lower() == j.lower()):
                alert = 0
    # --
    # luot nhung stopwords trong content cua post de thong ke sach hon
    f = codecs.open(
        file_path_stopwords, "r", "utf8")
    vnstopwords = f.read()
    vn_sw = vnstopwords.splitlines()
    clean_tokens = tokens[:]
    # bintrash = []
    for token in tokens:
        if token in vn_sw:
            clean_tokens.remove(token)
            # bintrash.append(token)

    print("--Length clean_tokens : "+str(len(clean_tokens)))
    print("--Length tokens : "+str(len(tokens)))
    # print("\n--Show clean token : "+str(clean_tokens))
    # print("\n--Show Bin : "+str(bintrash))

    # thong ke so luong tu sau khi luot stopwords trong post

    # freq = nltk.FreqDist(clean_tokens)

    # ve bieu do sau khi luot stopwords trong post
    # freq.plot(20, cumulative=False)

    # freq = nltk.FreqDist(tokens) # thong ke so luong tu day du trong post
    # for key,val in freq.items():
    #     print(str(key) + ':' + str(val))
    # --
    # print("Data push: "+company_name+" "+companyemail+" "+programminglanguage+" "+jobposition+" "+link_post+" "+text+" "+str(alert))
    database(company_name.capitalize(), companyemail, programminglanguage,
             jobposition, link_post, text.replace('description ', ''), alert)
    print("-------alert: "+str(alert))
    if(alert != 0):
        print("WARNING!-Day co kha nang cao la post khong lien quan!\n")
    else:
        print("Khong co canh bao nao!")
    f.close()
# func_DataAnalysis()


def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def newfunc_DataAnalysis():
    t1 = time.time()
    file_path = os.path.join(script_dir, "testnewmyfile20.txt")
    file_path_pl_train = os.path.join(script_dir, "train_NLTK/pl_train.txt")
    file_path_checkwords = os.path.join(
        script_dir, "train_NLTK/checkwords_vn_train.txt")
    f = codecs.open(file_path, "r", "utf8")
    txtjson = f.read()
    try:
        objjson = json.loads(txtjson)
    except:
        print("File json loi kiem tra lai!")
        quit()
    f.close()
    job_position_check = ["Senior", "Fresher",
                          "Intern", "Junior", "Tester", "Dev", "Software Test Intern", "Software Test Fresher"]
    company_syn = ["công ty", "cty"]
    job_position = []
    programming_language = []
    count = 0
    for i in range(len(objjson)):
        link_post = objjson[i]['post_url']
        desc_insertdb = remove_emojis(objjson[i]['description'])
        desc_analysis = re.sub(r"\W+|_", " ", desc_insertdb)
        tokens = word_tokenize(desc_analysis)
        # print(tokens)
        f = open(file_path_pl_train, "r")
        p_languges_raw = f.read()
        p_languges = p_languges_raw.split()
        f.close()
        company_email = re.findall(r'\S+@\S+', desc_insertdb)
        for i in company_syn:
            for j in range(len(tokens)):
                if(i.lower() == tokens[j].lower()):
                    company_name = tokens[j+1]
                    break
                else:
                    if company_email != None:
                        try:
                            company_name = (
                                ((company_email[0].split('.'))[0]).split('@'))[1]
                        except:
                            company_name = tokens[0]
                    else:
                        company_name = tokens[0]
            if(i.lower() == tokens[j].lower()):
                break
        for i in tokens:
            for j in job_position_check:
                if(i.lower() == j.lower()):
                    if(j not in job_position):
                        job_position.append(j)
        for i in desc_analysis.split():
            for j in p_languges:
                if(i.lower() == j.lower()):
                    if(j not in programming_language):
                        programming_language.append(j)
        # chuyen mang thanh chuoi push vao db
        x = ''
        y = ''
        z = ''
        for i in programming_language:
            x = x+i+", "
        programminglanguage = x.strip(", ")
        for i in list(set(company_email)):
            y = y+i+", "
        companyemail = y.strip(", ")
        for i in job_position:
            z = z+i+", "
        jobposition = z.strip(", ")
        # kiem tra co phai post spam khong
        f = codecs.open(file_path_checkwords, "r", "utf8")
        text_check = f.read()
        Arr_check = word_tokenize(text_check)
        alert = 1
        for i in tokens:
            for j in Arr_check:
                if(i.lower() == j.lower()):
                    alert = 0
        # push vao db
        print("------"+str(count+1)+"------")
        print("Company mail : "+companyemail
              + "| Company name : "+company_name.capitalize()
              + "| PL : "+programminglanguage
              + "| Job position : "+jobposition
              + "| Status: "+str(alert))
        database(company_name.capitalize(), companyemail, programminglanguage,
                 jobposition, link_post, desc_insertdb, alert)
        count = count + 1
    noti = "Xu ly "+str(len(objjson))+" post thanh cong "+str(count)+" post."
    print(noti)
    t2 = time.time()
    processingtime = "processing time: {:.3f}".format(t2-t1)
    print(processingtime)
    history_path = os.path.join(script_dir, "history.txt")
    history = codecs.open(
        history_path, "a", "utf8")
    dt = datetime.datetime.now()
    history.write(noti+" || "+processingtime+" || " +
                  dt.strftime("%x")+" "+dt.strftime("%X"))
    history.write("\n")
    history.close()
# newfunc_DataAnalysis()


def main():
    t1 = time.time()
    true = 1
    count = 1
    while true == 1:
        print("<"+str(count)+">")
        try:
            func_DataAnalysis()
            count = count+1
        except:
            count = count-1
            true = 0
    t2 = time.time()
    noti="Đã xử lí "+str(count)+" posts thành công . Hàng đợi hiện trống!"
    print(noti)
    processingtime = "processing time: {:.3f}".format(t2-t1)
    print('processingtime: '+processingtime)
    history_path = os.path.join(script_dir, "history.txt")
    history = codecs.open(
        history_path, "a", "utf8")
    dt = datetime.datetime.now()
    history.write(noti+" || "+processingtime+" || " +
                  dt.strftime("%x")+" "+dt.strftime("%X"))
    history.write("\n")
    history.close()
# main()


def trainCheckPost():
    func_TrainFor_checkSPAM()


def funcquit():
    print("Kết Thúc.")
    quit()


def funcOpenFileTrainCheckPost():
    file_path = os.path.join(script_dir, "train_NLTK/checkwords_vn_train.txt")
    f = codecs.open(
        file_path, "r", "utf8")
    keywords_for_check = f.read()
    ArrCheck = word_tokenize(keywords_for_check)
    print(str(ArrCheck)+"\n")


def funcOpenFileTrainPL():
    file_path = os.path.join(script_dir, "train_NLTK/pl_train.txt")
    f = codecs.open(
        file_path, "r", "utf8")
    keywords_for_check = f.read()
    ArrCheck = keywords_for_check.split()
    print(str(ArrCheck)+"\n")
