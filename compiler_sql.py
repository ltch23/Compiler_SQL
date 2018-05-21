#***************************************************************************************
import re
file = open('codesql.txt', 'r')
data = file.readlines()
file.close()
list_token = []

# print ("data: ",data)


def remove_comments(string):
    
    string = re.sub( re.compile("/*.*?\*/",re.DOTALL),"" ,string) # Remove /*comment */)
    
    string = re.sub(re.compile("--.*?\n") ,"" ,string) # Remove // comment\n 
    string = re.sub(re.compile("--.*?$") ,"" ,string) # Remove // comment\$  
    if (re.compile("/\*.*?\n"), "", string):
        string = re.sub(re.compile("/\*.*?\n"), "", string) # Remove /*comment 
        string = re.sub(re.compile(".*?\*"), "", string) # Remove comment/* 
   
    return string
#***************************************************************************************# Tokens Diccionary 
tkn_point = re.compile('.')
tkn_id = re.compile('[a-zA-Z]+[a-zA-Z1-9_]*')
tkn_num_int = re.compile('[0-9]+')
tkn_num_float = re.compile('[0-9]+.[0-9]+')
tkn_num_date = re.compile('\"[0-9]+\/[0-9]+\/[0-9]+\"')
tkn_num_time= re.compile('\"[0-9]+:[0-9]+:[0-9]+\"')
tkn_varchar = re.compile('\"[a-zA-Z]+[a-zA-Z1-9_]*\"')

#*************************************************************************************

def preprocesing():
    num_line = 1
    list_splits=[]
    for renglon in data:
        uncommetns = remove_comments(renglon)
        uncommetns = uncommetns.split(' ')
        for word in  uncommetns:
            separators= r"([+]|-|[*]|;|,|<=|>=|<|>|=|\n|[(]|[)]|[[]|[]]|{|})"
            splits= re.split(separators, word)
            list_splits = filter(None,splits)
            
            for lexem in list_splits:
                tmp= re.split(r"([.])", lexem)
                if re.match(tkn_id, tmp[0]):
                    m = re.match(tkn_id, tmp[0])
                    if len(m.group(0)) == len(tmp[0]):
                        if len(tmp)==3:   
                            if tmp[1]==".":
                                lexem=('\n')
                                list_token.append([tmp[0],"tkn_undefined",num_line])
                                list_token.append([tmp[1],"tkn_undefined",num_line])
                                list_token.append([tmp[2],"tkn_undefined",num_line])
                                    # print(len(tmp))   
                if(lexem != ('\n')):
                    list_token.append([lexem,"tkn_undefined",num_line])
        num_line +=1    

#***************************************************************************************
def print_lt():
    for token in list_token:
        print (token)
#***************************************************************************************



tkn_list = [["select","tkn_select"],["insert","tkn_insert_into"],["update","tkn_update"],["delete","tkn_delete"],
            ["from","tkn_from"],["where","tkn_where"],["*","tkn_*"], ["avg","tkn_avg"],["sum","tkn_sum"],["count","tkn_count"],
            ["group_by","tkn_group_by"],["order_by","tkn_order_by"],["inner_join","tkn_inner_join"],["on","tkn_on"],["values","tkn_values"],["set","tkn_set"],
            ["(","tkn_("],[")","tkn_)"],[";",";"],[",","tkn_,"],
            ["=","tkn_="],["<","tkn_<"],[">","tkn_>"],["<=","tkn_<="],[">=","tkn_>="],
            ["and","tkn_and"],["or","tkn_or"],["not","tkn_not"],
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
                    # if token < len(list_token)-1:   
                    #     if re.match(tkn_point, list_token[token+1][0]):
                    #         m = re.match(tkn_point, list_token[token+1][0])
                    #         if len(m.group(0)) == len(list_token[token+1][0]):
                    #             list_token[token+1][1] = "tkn_."
                    
                # else:
                #     print ("Error string not found in the line: ", list_token[token][2])
            
            if re.match(tkn_varchar, list_token[token][0]):
                m = re.match(tkn_varchar, list_token[token][0])
                if len(m.group(0)) == len(list_token[token][0]):
                    list_token[token][1] = "tkn_varchar"
                # else:
                #     print ("Error string not found in the line: ", list_token[token][2])

            if re.match(tkn_point, list_token[token][0]):
                m = re.match(tkn_point, list_token[token][0])
                if len(m.group(0)) == len(list_token[token][0]):
                    list_token[token][1] = "tkn_."
                # else:
                #     print ("Error string not found in the line: ", list_token[token][2])
            if re.match(tkn_num_date, list_token[token][0]):
                m = re.match(tkn_num_date, list_token[token][0])
                if len(m.group(0)) == len(list_token[token][0]):
                    list_token[token][1] = "tkn_date"
                # else:
                #     print ("Error string not found in the line: ", list_token[token][2])
            if re.match(tkn_num_time, list_token[token][0]):
                m = re.match(tkn_num_time, list_token[token][0])
                if len(m.group(0)) == len(list_token[token][0]):
                    list_token[token][1] = "tkn_time"
                else:
                    print ("Error string not found in the line: ", list_token[token][2])
            # if re.match(tkn_varchar, list_token[token][0]):
            if re.match(tkn_num_float, list_token[token][0]):
                m = re.match(tkn_num_float, list_token[token][0])
                if len(m.group(0)) == len(list_token[token][0]):
                    list_token[token][1] = "tkn_float"
                # else:
                #     print ("Error string not found in the line: ", list_token[token][2])
            #     m = re.match(tkn_varchar, list_token[token][0])
            if re.match(tkn_num_int, list_token[token][0]):
                m = re.match(tkn_num_int, list_token[token][0])
                if len(m.group(0)) == len(list_token[token][0]):
                    list_token[token][1] = "tkn_int"
                # else:
                #     print ("Error string not found in the line: ", list_token[token][2])
            

            if list_token[token][1]=="tkn_undefined":
                print("print ",[list_token[token][0],list_token[token][1],list_token[token][2]])
                list_token[token].pop()
                list_token[token].pop()
                list_token[token].pop()
            #     #bitacora
#***************************************************************************************


table_sim = {}

def tabla_sim():
    for t in range(0,len(list_token)):
        if list_token[t][1] == "tkn_id": # and list_token[t][1] != "tkn_undefined":
            if list_token[t][0] not in table_sim:
                 table_sim[list_token[t][0]]= {'Lexem':list_token[t][1], 'Value': '','Len': len(list_token[t][0]), 'Data_type':'','ifTC':'','Line': list_token[t][2]}

            # else:


                 # table_sim[list_token[id][0]]['Line'].append(list_token[id][2])

#***************************************************************************************

def print_TS():
    for key in table_sim:
        print (key, ":", table_sim[key])
#***************************************************************************************



terminals = {
'tkn_select':1,'tkn_insert_into':2,'tkn_update':3,'tkn_delete':4,'tkn_avg':5,'tkn_sum':6,'tkn_count':7,'tkn_from':8,'tkn_inner_join':9,'tkn_on':10,'tkn_where':11,'tkn_group_by':12,'tkn_order_by':13,'tkn_values':14,'tkn_set':15,'tkn_*':16,'tkn_id':17,'tkn_.':18,'tkn_(':19,'tkn_)':20,'tkn_and':21,'tkn_or':22,'tkn_<':23,'tkn_>':24,'tkn_<=':25,'tkn_>=':26,'tkn_=':27,'tkn_,':28,'tkn_int':29,'tkn_float':30,'tkn_time':31,'tkn_date':32,'tkn_varchar':33,'$':34,
}


no_terminals = {
'A':1,'S':2,'F':3,'J':4,'W':5,'G':6,'I':7,'U':8,'op_rel':9,'op_com':10,'numeros':11,'valor_s':12,'valor_c':13,'valores':14,'id_tmp':15,'id_sim':16,'id_com':17,'ids':18,'C':19,'id_val':20,'cond_sim':21,'cond_com':22,'conditions':23,'set_sim':24,'set_com':25,'sets':26,
}



table_syntactic = {
1:['tkn_select', 'S','F','J','W','G'],   2:['tkn_insert_into', 'I'], 3:['tkn_update', 'U','W'], 4:['tkn_delete','F','W'], 5:[''],6:[''],7:[''],8:[''],9:[''],10:[''],11:[''],12:[''],13:[''],14:[''],15:[''],16:[''],17:[''],18:[''],19:[''],20:[''],21:[''],22:[''],23:[''],24:[''],25:[''],26:[''],27:[''],28:[''],29:[''],30:[''],31:[''],32:[''],33:[''],34:[''],

35:[''],36:[''],37:[''],38:[''],39:['C','tkn_(','ids','tkn_)'],40:['C','tkn_(','ids','tkn_)'],41:['C','tkn_(','ids','tkn_)'],42:[''],43:[''],44:[''],45:[''],46:[''],47:[''],48:[''],49:[''],50:['tkn_*'],51:['ids'],52:[''],53:[''],54:[''],55:[''],56:[''],57:[''],58:[''],59:[''],60:[''],61:[''],62:[''],63:[''],64:[''],65:[''],66:[''],67:[''],68:[''],

69:[''],70:[''],71:[''],72:[''],73:[''],74:[''],75:[''],76:['tkn_from','ids'],77:[''],78:[''],79:[''],80:[''],81:[''],82:[''],83:[''],84:[''],85:[''],86:[''],87:[''],88:[''],89:[''],90:[''],91:[''],92:[''],93:[''],94:[''],95:[''],96:[''],97:[''],98:[''],99:[''],100:[''],101:[''],102:[''],

103:[''],104:[''],105:[''],106:[''],107:[''],108:[''],109:[''],110:[''],111:['tkn_inner_join','id_sim','tkn_on','id_sim','tkn_=','id_sim','J'],112:[''],113:['vacio'],114:['vacio'],115:[''],116:[''],117:[''],118:[''],119:[''],120:[''],121:[''],122:[''],123:[''],124:[''],125:[''],126:[''],127:[''],128:[''],129:[''],130:[''],131:[''],132:[''],133:[''],134:[''],135:[''],136:['vacio'],

137:[''],138:[''],139:[''],140:[''],141:[''],142:[''],143:[''],144:[''],145:[''],146:[''],147:['tkn_where','conditions'],148:['vacio'],149:[''],150:[''],151:[''],152:[''],153:[''],154:[''],155:[''],156:[''],157:[''],158:[''],159:[''],160:[''],161:[''],162:[''],163:[''],164:[''],165:[''],166:[''],167:[''],168:[''],169:[''],170:['vacio'],

171:[''],172:[''],173:[''],174:[''],175:[''],176:[''],177:[''],178:[''],179:[''],180:[''],181:[''],182:['tkn_group_by','ids','tkn_order_by','ids'],183:['tkn_group_by','ids','tkn_order_by','ids'],184:[''],185:[''],186:[''],187:[''],188:[''],189:[''],190:[''],191:[''],192:[''],193:[''],194:[''],195:[''],196:[''],197:[''],198:[''],199:[''],200:[''],201:[''],202:[''],203:[''],204:['vacio'],

205:[''],206:[''],207:[''],208:[''],209:[''],210:[''],211:[''],212:[''],213:[''],214:[''],215:[''],216:[''],217:[''],218:[''],219:[''],220:[''],221:['tkn_id','tkn_values','tkn_(','valores','tkn_)'],222:[''],223:[''],224:[''],225:[''],226:[''],227:[''],228:[''],229:[''],230:[''],231:[''],232:[''],233:[''],234:[''],235:[''],236:[''],237:[''],238:[''],

239:[''],240:[''],241:[''],242:[''],243:[''],244:[''],245:[''],246:[''],247:[''],248:[''],249:[''],250:[''],251:[''],252:[''],253:[''],254:[''],255:['tkn_id','tkn_set','sets'],256:[''],257:[''],258:[''],259:[''],260:[''],261:[''],262:[''],263:[''],264:[''],265:[''],266:[''],267:[''],268:[''],269:[''],270:[''],271:[''],272:[''],

273:[''],274:[''],275:[''],276:[''],277:[''],278:[''],279:[''],280:[''],281:[''],282:[''],283:[''],284:[''],285:[''],286:[''],287:[''],288:[''],289:[''],290:[''],291:[''],292:[''],293:['tkn_and'],294:['tkn_or'],295:[''],296:[''],297:[''],298:[''],299:[''],300:[''],301:[''],302:[''],303:[''],304:[''],305:[''],306:[''],

307:[''],308:[''],309:[''],310:[''],311:[''],312:[''],313:[''],314:[''],315:[''],316:[''],317:[''],318:[''],319:[''],320:[''],321:[''],322:[''],323:[''],324:[''],325:[''],326:[''],327:[''],328:[''],329:['tkn_<'],330:['tkn_>'],331:['tkn_<='],332:['tkn_>='],333:['tkn_='],334:[''],335:[''],336:[''],337:[''],338:[''],339:[''],340:[''],

341:[''],342:[''],343:[''],344:[''],345:[''],346:[''],347:[''],348:[''],349:[''],350:[''],351:[''],352:[''],353:[''],354:[''],355:[''],356:[''],357:[''],358:[''],359:[''],360:[''],361:[''],362:[''],363:[''],364:[''],365:[''],366:[''],367:[''],368:[''],369:['tkn_int'],370:['tkn_float'],371:['tkn_time'],372:['tkn_date'],373:[''],374:[''],

375:[''],376:[''],377:[''],378:[''],379:[''],380:[''],381:[''],382:[''],383:[''],384:[''],385:[''],386:[''],387:[''],388:[''],389:[''],390:[''],391:[''],392:[''],393:[''],394:[''],395:[''],396:[''],397:[''],398:[''],399:[''],400:[''],401:[''],402:[''],403:['numeros'],404:['numeros'],405:['numeros'],406:['numeros'],407:['tkn_varchar'],408:[''],

409:[''],410:[''],411:[''],412:[''],413:[''],414:[''],415:[''],416:[''],417:[''],418:[''],419:[''],420:[''],421:[''],422:[''],423:[''],424:[''],425:[''],426:[''],427:[''],428:['vacio'],429:[''],430:[''],431:[''],432:[''],433:[''],434:[''],435:[''],436:['tkn_,','valor_s','valor_c'],437:[''],438:[''],439:[''],440:[''],441:[''],442:[''],

443:[''],444:[''],445:[''],446:[''],447:[''],448:[''],449:[''],450:[''],451:[''],452:[''],453:[''],454:[''],455:[''],456:[''],457:[''],458:[''],459:[''],460:[''],461:[''],462:[''],463:[''],464:[''],465:[''],466:[''],467:[''],468:[''],469:[''],470:[''],471:['valor_s','valor_c'],472:['valor_s','valor_c'],473:['valor_s','valor_c'],474:['valor_s','valor_c'],475:['valor_s','valor_c'],476:[''],

477:[''],478:[''],479:[''],480:[''],481:[''],482:[''],483:[''],484:['vacio'],485:['vacio'],486:['vacio'],487:['vacio'],488:['vacio'],489:['vacio'],490:['vacio'],491:['vacio'],492:[''],493:[''],494:['tkn_.','tkn_id'],495:[''],496:['vacio'],497:['vacio'],498:['vacio'],499:['vacio'],500:['vacio'],501:['vacio'],502:['vacio'],503:['vacio'],504:['vacio'],505:[''],506:[''],507:[''],508:[''],509:[''],510:['vacio'],

511:[''],512:[''],513:[''],514:[''],515:[''],516:[''],517:[''],518:[''],519:[''],520:[''],521:[''],522:[''],523:[''],524:[''],525:[''],526:[''],527:['tkn_id','id_tmp'],528:[''],529:[''],530:[''],531:[''],532:[''],533:[''],534:[''],535:[''],536:[''],537:[''],538:[''],539:[''],540:[''],541:[''],542:[''],543:[''],544:[''],

545:[''],546:[''],547:[''],548:[''],549:[''],550:[''],551:[''],552:['vacio'],553:['vacio'],554:[''],555:['vacio'],556:['vacio'],557:['vacio'],558:['vacio'],559:[''],560:[''],561:[''],562:[''],563:[''],564:['vacio'],565:[''],566:[''],567:[''],568:[''],569:[''],570:[''],571:[''],572:['tkn_,','id_sim','id_com'],573:[''],574:[''],575:[''],576:[''],577:[''],578:['vacio'],

579:[''],580:[''],581:[''],582:[''],583:[''],584:[''],585:[''],586:[''],587:[''],588:[''],589:[''],590:[''],591:[''],592:[''],593:[''],594:[''],595:['id_sim','id_com'],596:[''],597:[''],598:[''],599:[''],600:[''],601:[''],602:[''],603:[''],604:[''],605:[''],606:[''],607:[''],608:[''],609:[''],610:[''],611:[''],612:['vacio'],

613:[''],614:[''],615:[''],616:[''],617:['avg'],618:['sum'],619:['count'],620:[''],621:[''],622:[''],623:[''],624:[''],625:[''],626:[''],627:[''],628:[''],629:[],630:[''],631:[''],632:[''],633:[''],634:[''],635:[''],636:[''],637:[''],638:[''],639:[''],640:[''],641:[''],642:[''],643:[''],644:[''],645:[''],646:[''],

647:[''],648:[''],649:[''],650:[''],651:[''],652:[''],653:[''],654:[''],655:[''],656:[''],657:[''],658:[''],659:[''],660:[''],661:[''],662:[''],663:['id_sim'],664:[''],665:[''],666:[''],667:[''],668:[''],669:[''],670:[''],671:[''],672:[''],673:[''],674:[''],675:['valor_s'],676:['valor_s'],677:['valor_s'],678:['valor_s'],679:['valor_s'],680:[''],

681:[''],682:[''],683:[''],684:[''],685:[''],686:[''],687:[''],688:[''],689:[''],690:[''],691:[''],692:[''],693:[''],694:[''],695:[''],696:[''],697:['id_sim','op_com','id_val'],698:[''],699:[''],700:[''],701:[''],702:[''],703:[''],704:[''],705:[''],706:[''],707:[''],708:[''],709:[''],710:[''],711:[''],712:[''],713:[''],714:[''],

715:[''],716:[''],717:[''],718:[''],719:[''],720:[''],721:[''],722:[''],723:[''],724:[''],725:[''],726:['vacio'],727:[''],728:[''],729:[''],730:[''],731:[''],732:[''],733:[''],734:[''],735:['op_rel','cond_sim','cond_com'],736:['op_rel','cond_sim','cond_com'],737:[''],738:[''],739:[''],740:[''],741:[''],742:[''],743:[''],744:[''],745:[''],746:[''],747:[''],748:['vacio'],

749:[''],750:[''],751:[''],752:[''],753:[''],754:[''],755:[''],756:[''],757:[''],758:[''],759:[''],760:[''],761:[''],762:[''],763:[''],764:[''],765:['cond_sim','cond_com'],766:[''],767:[''],768:[''],769:[''],770:[''],771:[''],772:[''],773:[''],774:[''],775:[''],776:[''],777:[''],778:[''],779:[''],780:[''],781:[''],782:[''],

783:[''],784:[''],785:[''],786:[''],787:[''],788:[''],789:[''],790:[''],791:[''],792:[''],793:[''],794:[''],795:[''],796:[''],797:[''],798:[''],799:['id_sim','tkn_=','valor_s'],800:[''],801:[''],802:[''],803:[''],804:[''],805:[''],806:[''],807:[''],808:[''],809:[''],810:[''],811:[''],812:[''],813:[''],814:[''],815:[''],816:[''],

817:[''],818:[''],819:[''],820:[''],821:[''],822:[''],823:[''],824:[''],825:[''],826:[''],827:['vacio'],828:[''],829:[''],830:[''],831:[''],832:[''],833:[''],834:[''],835:[''],836:[''],837:[''],838:[''],839:[''],840:[''],841:[''],842:[''],843:[''],844:['tkn_,','set_sim','set_com'],845:[''],846:[''],847:[''],848:[''],849:[''],850:['vacio'],

851:[''],852:[''],853:[''],854:[''],855:[''],856:[''],857:[''],858:[''],859:[''],860:[''],861:[''],862:[''],863:[''],864:[''],865:[''],866:[''],867:['set_sim','set_com'],868:[''],869:[''],870:[''],871:[''],872:[''],873:[''],874:[''],875:[''],876:[''],877:[''],878:[''],879:[''],880:[''],881:[''],882:[''],883:[''],884:[''],
}



def tabla_syntac():
    while(len(l_imput)>0) :
        print ("Pila:", pila[::-1])
        print ("lexema:", l_lexem)
        
        if pila[0] in terminals:
            if (l_imput[0] == pila[0]):
                # print("- ",l_imput[0],pila[0])
                if l_imput[0] == '$' and pila[0] == '$':
                    print("String acepted")
                pila.pop(0)
                l_imput.pop(0)
                l_lexem.pop(0)
                l_line.pop(0)
            else:
                print("Error syntactic-  Token was not expected:" , l_imput[0],"line: ",l_line[0])
                pila.pop(0)
                l_imput.pop(0)
                l_lexem.pop(0)
                l_line.pop(0)

        else:
            # if pila[0].isdigit():
            #     pila.pop(0)
            # else:
                row = no_terminals[pila[0]] - 1

                col = terminals[l_imput[0]]
                # print("row ",row," col ",col,   "data", row * 34 + col)
                empila = table_syntactic[row * 34 + col]
                empilar = empila[::-1]
                print ('empila: ', empilar)
                pila.pop(0)
                for j in range(0,len(empilar)):
                    if(empilar[j] == ''):
                        print(">Error syntactic:  Token was not expected:" , l_imput[0],"line: ",l_line[0])
                        
                        # pila.pop(0)
                        l_imput.pop(0)
                        l_lexem.pop(0)
                        l_line.pop(0)
                        # print ("e:" ,l_imput)
                        # print ("l:" ,l_lexem)
                    elif(empilar[j] != 'vacio'):
                        pila.insert(0,empilar[j])


        # if not pila:
        #     return




preprocesing()
tokens()
print_lt()

tabla_sim()
print_TS()

pila=['A','$']
l_imput = []
l_lexem = []  
l_line = []  



for x in range(0, len(list_token)):
    l_imput.append(list_token[x][1])
    l_lexem.append(list_token[x][0])
    l_line.append(list_token[x][2])

l_imput.append('$')
l_lexem.append('$')


print ('**************************************')
print ("l_imput ",l_imput)
print ("l_lexem ",l_lexem)
print ("pila ",pila)



tabla_syntac()



class NoTerminal:
    def __init__(self):
        self.lexem = None  #  acceder a  TS en la pos "lexema"
        self.type = None
        self.value = None
        self.ifTC = None

# Inicializar No Terminales
# -----------------------------------------------------------------------------

A = NoTerminal()
S = NoTerminal()
C = NoTerminal()
F = NoTerminal()
J = NoTerminal()
W = NoTerminal()
G = NoTerminal()
I = NoTerminal()
U = NoTerminal()
op_rel = NoTerminal()
op_com = NoTerminal()
numeros = NoTerminal()
valor_s = NoTerminal()
valor_c = NoTerminal()
valores = NoTerminal()
id_tmp = NoTerminal()
id_sim = NoTerminal()
id_com = NoTerminal()
ids = NoTerminal()
id_val = NoTerminal()
cond_sim = NoTerminal()
cond_com = NoTerminal()
conditions = NoTerminal()
set_sim = NoTerminal()
set_com = NoTerminal()
sets = NoTerminal()


# Reglas Semanticas
def operacion(objeto1,objeto2,operador):
    if operador == '+':
        return objeto1 + objeto2
    elif operador == '-':
        return objeto1 - objeto2
    elif operador == '=':
        return objeto1 == objeto2
    elif operador == '!=':
        return objeto1 != objeto2
    elif operador == '>=':
        return objeto1 >= objeto2
    elif operador == '<=':
        return objeto1 <= objeto2
    elif operador == '>':
        return objeto1 > objeto2
    elif operador == '<':
        return objeto1 < objeto2

def get_value(id):
    return tabla_sim[id]['Value']

def get_lexema(id):
    return tabla_sim[id]['Lexema']

def get_ifTC(id):
    return tabla_sim[id]['ifTC']

def get_type(id):
    return tabla_sim[id]['Type']

def set_value(id,value):
    tabla_sim[id]['Value'] = value

def set_type(id,type):
    tabla_sim[id]['Type'] = type

#tabla 0 - col 1
def set_ifTC(id):
    tabla_sim[id]['ifTC'] = 0 


# Comprobación de types && Paso de Valor
def rule_1(objeto1,objeto2):
    if objeto1.type == objeto2.type:
        objeto1.value = objeto2.value
    else:
        print ("Error de type")

# Comprobacion de types && set_value
def rule_2(objeto1,id):
    if objeto1.type == get_type(id):
        set_value(id,objeto1.value)
    else:
        print ("Error de type")

# Paso de type
def rule_3(objeto1, objeto2):
    objeto1.type = objeto2.type

# Sintetizado type
def rule_4(objeto1, objeto2):
    objeto1.type = objeto2

# Paso de type && Paso de Lexema
def rule_6(objeto1,objeto2,id):
    objeto1.type = objeto2.type
    objeto1.lexema = get_lexema(id)


# Paso de type y Valor
def rule_7(objeto1, objeto2):
    objeto1.type = objeto2.type
    objeto1.value = objeto2.value


# get_type && get_value && get_lexema
def rule_8(objeto1, id):
    objeto1.type = get_type(id)
    objeto1.value = get_value(id)
    objeto1.lexema = get_lexema(id)



# Sintetizado lexem
def rule_9(objeto1, objeto2):
    objeto1.lexema = objeto2

# Paso de Lexema
def rule_10(objeto1, objeto2):
    objeto1.lexema = objeto2.lexema


#Condicion o setting
def rule_11(objeto1,objeto2):
    if objeto1.type != objeto2.type:
        print ("Error de type")

# Operaciones Aritméticas
def rule_op_ari(objeto1, objeto2,operador):
    if objeto1.type == objeto2.type:
        objeto1.value = operacion (objeto1.value,objeto2.value,operador.lexema)
    print ("Error de type")

# Operaciones comparaciob
def rule_op_rel(objeto1, objeto2,objeto3, operador):
    if objeto1.type == objeto2.type:
        objeto3.value = operacion(objeto1.value, objeto2.value, operador.lexema)
        objeto3.type = 'tkn_bool'
    else:
        print ("Error de types")

