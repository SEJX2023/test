def say_hello(times, language):
    if language == "CHINESE" or language==1:
        print("times = "+str(times)+" ; language is "+"Chinese.")
        for i in range(times):
            print("你好！")
    elif language == "RUSSIAN" or language==2:
        print("times = " + str(times) + " ; language is " + "English.")
        for i in range(times):
            print("Привет!")
    elif language == "ENGLISH" or language==3:
        print("times = " + str(times) + " ; language is " + "English.")
        for i in range(times):
            print("Hello!")

while 1:
    times=int(input("Please input repeat times(such as 1, 2, etc):\n"))
    language=input("Please input language(such as Russian, or 2):\n\t1-Chinese; 2-Russian; 3-English\n")
    length=len(language)
    if length>1:
        language=language.upper()
        say_hello(times,language)
    elif length==1:
        say_hello(times,int(language))
    break
