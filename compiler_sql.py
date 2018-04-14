#***************************************************************************************
import re
file = open('codesql.txt', 'r')
data = file.readlines()
file.close()
list_token = []

print ("data: ",data)


def remove_comments(string):
    
    string = re.sub( re.compile("/*.*?\*/",re.DOTALL),"" ,string) # Remove /*comment */)
    
    string = re.sub(re.compile("--.*?\n") ,"" ,string) # Remove // comment\n 
    string = re.sub(re.compile("--.*?$") ,"" ,string) # Remove // comment\$  
    if (re.compile("/\*.*?\n"), "", string):
        string = re.sub(re.compile("/\*.*?\n"), "", string) # Remove /*comment 
        string = re.sub(re.compile(".*?\*"), "", string) # Remove comment/* 
   
    return string
#***************************************************************************************

def preprocesing():
    num_line = 1
    list_splits=[]
    for renglon in data:
        uncommetns = remove_comments(renglon)
        uncommetns = uncommetns.split(' ')
        for word in  uncommetns:
            separators= r"([+]|-|[*]|[/]|;|,|=|<=|>=|<|>|[(]|[)]|[[]|[]]|{|})"
            splits= re.split(separators, word)
            list_splits = filter(None,splits)
            for lexem in list_splits:
                if(lexem != ('\n')):
                    list_token.append([lexem,"tkn_undefined",num_line])
        num_line +=1    
#***************************************************************************************


# Tokens Diccionary 
tkn_id = re.compile('[a-zA-Z]+[a-zA-Z1-9_]*')
tkn_num = re.compile('[0-9]+')

tkn_list = [["int","tkn_int"],["varchar","tkn_varchar"],["date","tkn_date"],["time","tkn_time"],
            ["select","tkn_select"],["insert","tkn_insert"],["update","tkn_update"],["delete","tkn_delete"],
            ["from","tkn_from"],["where","tkn_where"],["all","tkn_all"],["values","tkn_values"],
            ["(","("],[")",")"],[";",";"],[",",","],
            ["=","="],["<","<"],[">",">"],["<=","<="],["==","=="],["!=","!="],
            ["and","tkn_and"],["or","tkn_or"],["not","tkn_not"],
            ["+","+"],["-","-"],["*","*"],["/","/"],
            ]


def tokens():

    for token in range(0,len(list_token)):
        
        for i in range(0,len(tkn_list)):
            if list_token[token][0] == tkn_list[i][0]:
                list_token[token][1] = tkn_list[i][1]

        if list_token[token][1]=="tkn_undefined":

            if re.match(tkn_id, list_token[token][0]):
                m = re.match(tkn_id, list_token[token][0])
                if len(m.group(0)) == len(list_token[token][0]):
                    list_token[token][1] = "tkn_id"
                else:
                    print ("Error string not found in the line: ", list_token[token][2])

            elif re.match(tkn_num, list_token[token][0]):
                m = re.match(tkn_num, list_token[token][0])
                if len(m.group(0)) == len(list_token[token][0]):
                    list_token[token][1] = "tkn_num"
                else:
                    print ("Error string not found in the line: ", list_token[token][2])
                #bitacora
#***************************************************************************************

table_sim = {}

def tabla_sim():
    for id in range(0,len(list_token)):
        if list_token[id][1] == "tkn_id":
            if not list_token[id][0] in table_sim:
                table_sim[list_token[id][0]] ={'Lexem': list_token[id][0], 'Value': '','Tam': '', 'Data_type':'','Line': [list_token[id][2]]}
            else:
                table_sim[list_token[id][0]]['Line'].append(list_token[id][2])

#***************************************************************************************

def print_ts():
    for key in table_sim:
        print (key, ":", table_sim[key])
#***************************************************************************************


preprocesing()
tokens()
#print (list_token)
tabla_sim()
print_TS()
