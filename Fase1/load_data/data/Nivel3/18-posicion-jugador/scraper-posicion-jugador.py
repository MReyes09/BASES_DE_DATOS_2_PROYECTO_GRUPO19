#!/usr/bin/env python3
"""
SCRAPER PLANTILLA + POSICION_JUGADOR
Genera:
  - 10plantilla.sql              -> INSERT INTO Plantilla
  - 18posicionjugador.sql        -> INSERT INTO Posicion_Jugador
  - jugadores_no_encontrados.txt -> Jugadores sin match en 03jugador.sql
"""

import re
import unicodedata
import difflib
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime


# ─────────────────────────────────────────────
#  RUTAS
# ─────────────────────────────────────────────
HTML_DIR           = Path(r"C:\Users\DILAN\Documents\USAC\Bases2\Archivos\html_informacion_partido\html")
PAIS_SQL           = Path(r"C:\Users\DILAN\Documents\USAC\Bases2\Proyecto\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\05-pais\5pais.sql")
JUGADOR_SQL        = Path(r"C:\Users\DILAN\Documents\USAC\Bases2\Proyecto\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\03-jugador\3jugador.sql")

OUT_PLANTILLA      = Path("./10plantilla.sql")
OUT_POSICION       = Path("./18posicionjugador.sql")
OUT_NO_ENCONTRADOS = Path("./jugadores_no_encontrados.txt")


# ─────────────────────────────────────────────
#  ALIAS DE PAISES
# ─────────────────────────────────────────────
PAIS_ALIAS = {
    "Emiratos Arabes"           : "Emiratos Árabes Unidos",
    "Paises Bajos"              : "Países Bajos",
    "Iraq"                      : "Irak",
    "Indias Orientales Holand." : "Indonesia",
    "RF de Yugoslavia"          : "Yugoslavia",
    "Serbia y Montenegro"       : "Serbia",
}


# ─────────────────────────────────────────────
#  ALIAS DE JUGADORES
#  Clave = nombre normalizado del HTML
#  Valor = int (id directo) o str (nombre en 03jugador.sql)
# ─────────────────────────────────────────────
ALIAS_JUGADORES = {
    # ── ID directo ──
    "pele"                          : 6050,
    "pelé"                          : 6050,

    # ── Nombre completo en SQL ──
    "michele andreolo"              : "miguel andreolo frodella",
    "miguel andreolo"               : "miguel andreolo frodella",
    "garrincha"                     : "manuel francisco dos santos",
    "bobby charlton"                : "sir robert charlton",
    "johan cruijff"                 : "hendrik johannes cruijff",
    "johan cruyff"                  : "hendrik johannes cruijff",
    "michel platini"                : "michel françois platini",
    "diego maradona"                : "diego armando maradona",
    "emilio butragueno"             : "emilio butragueño santos",
    "emilio butragueño"             : "emilio butragueño santos",
    "paolo maldini"                 : "paolo cesare maldini",
    "roberto carlos"                : "roberto carlos da silva rocha",
    "ronaldinho"                    : "ronaldo de assis moreira",
    "ronaldinho gaúcho"             : "ronaldo de assis moreira",
    "ronaldinho gaucho"             : "ronaldo de assis moreira",
    "thierry henry"                 : "thierry daniel henry",
    "andres iniesta"                : "andrés iniesta luján",
    "maicon"                        : "maicon douglas sisenando",
    "sergio ramos"                  : "sergio ramos garcía",
    "xavi"                          : "xavi simons",
    "angel di maria"                : "ángel fabián di maría hernández",
    "ángel di maría"                : "ángel fabián di maría hernández",
    "david luiz"                    : "david luiz moreira marinho3",
    "lionel messi"                  : "lionel andrés messi",
    "manuel neuer"                  : "manuel peter neuer",
    "marcelo"                       : "marcelo vieira da silva júnior",
    "mats hummels"                  : "mats julian hummels",
    "neymar jr."                    : "neymar da silva santos júnior",
    "neymar jr"                     : "neymar da silva santos júnior",
    "neymar"                        : "neymar da silva santos júnior",
    "thiago silva"                  : "thiago emiliano da silva",
    "cristiano ronaldo"             : "cristiano ronaldo dos santos aveiro",
    "diego godin"                   : "diego roberto godín leal",
    "eden hazard"                   : "eden michael hazard",
    "harry kane"                    : "harry edward kane",
    "kylian mbappe"                 : "kylian mbappé lottin",
    "kylian mbappé"                 : "kylian mbappé lottin",
    "philippe coutinho"             : "philippe coutinho correia",
    "raphael varane"                : "raphaël xavier varane",
    "raphael xavier varane"         : "raphaël xavier varane",
    "romelu lukaku"                 : "romelu menama lukaku bolingoli",
    "thibaut courtois"              : "thibaut nicolas marc courtois",
    "paul pogba"                    : "paul labile pogba",
    "emiliano martínez"             : "damián emiliano martínez",
    "emiliano martinez"             : "damián emiliano martínez",
    "aaron lennon"                  : "aaron justin lennon",
    "aaron mooy"                    : "aaron frank mooy",
    "abdelkarim hassan"             : "abdelkarim hassan al haj fadlalla",
    "abdiel arroyo"                 : "abdiel arroyo molinar",
    "abdullah zubromawi"            : "abdullah sulaiman zubromawi",
    "abel aguilar"                  : "abel enrique aguilar tapias",
    "achraf hakimi"                 : "achraf hakimi mouh",
    "adolfo machado"                : "adolfo abdiel machado",
    "adrien silva"                  : "adrien sébastien perruchet da silva",
    "ahmed elmohamady"              : "ahmed eissa elmohamady abdel fattah",
    "ahmed hegazi"                  : "ahmed elsayed ali elsayed hegazy",
    "ahmed khalil"                  : "ahmed khalil sebait mubarak al-junaibi",
    "akram afif"                    : "akram hassan afif yahya afif alyafei",
    "alan a'court"                  : "Alan A'Court",
    "alan dzagoev"                  : "alan yelizbarovich dzagoev",
    "alan pulido"                   : "alan pulido izaguirre",
    "aldo corzo"                    : "aldo sebastián corzo chávez",
    "alejandro gomez"               : "alejandro darío gómez",
    "aleksandr golovin"             : "aleksandr sergeyevich golovin",
    "aleksandr samedov"             : "aleksandr sergeyevich samedov",
    "aleksandr yerokhin"            : "aleksandr yuryevich yerokhin",
    "aleksei miranchuk"             : "aleksei andreyevich miranchuk",
    "alex iwobi"                    : "alexander chuka iwobi",
    "alex sandro"                   : "alex sandro lobo silva",
    "alex telles"                   : "alex nicolao telles",
    "alexander bah"                 : "alexander hartmann bah",
    "alexis sanchez"                : "alexis alejandro sánchez sánchez",
    "alfred gomis"                  : "alfred benjamin gomis",
    "alfred n'diaye"                : "alfred john momar n''diaye",
    "alfredo di stefano"            : "",
    "ali al-bulaihi"                : "ali hadi al-bulaihi",
    "ali el-said"                   : "ali mohammed el-kaf el-said",
    "ali gabr"                      : "ali gabr gabr mossad",
    "ali gholizadeh"                : "ali gholizadeh nojedeh",
    "alireza jahanbakhsh"           : "alireza jahanbakhsh jirandeh",
    "alisson"                       : "alisson ramses becker",
    "alistair johnston"             : "alistair william johnston",
    "almoez ali"                    : "almoez ali zainalabedeen mohamed abdulla",
    "alphonso davies"               : "alphonso boyle davies",
    "amadou onana"                  : "amadou zeund georges ba mvom onana",
    "amir hossein sadeghi"          : "amir hossein sadeghi or sadeqi",
    "amr warda"                     : "amr medhat warda",
    "anderson santamaria"           : "anderson santamaría bardales",
    "andranik teymourian"           : "andranik timotian-samarani",
    "andreas christensen"           : "andreas bødtker christensen",
    "andres guardado"               : "josé andrés guardado hernández",
    "andrew redmayne"               : "andrew james redmayne",
    "andrey lunyov"                 : "andrey yevgenyevich lunyov",
    "alan a'court": "Alan A'Court",
    "alfred n'diaye": "alfred john momar n'diaye",
    "andrey semenov": "andrey sergeyevich semenov",
    "andre carrillo": "andré martín carrillo díaz",
    "andre onana": "andré onana onana",
    "andre silva": "andré miguel valente da silva",
    "andy polo": "andy jorman polo andrade",
    "anthony contreras": "anthony daniel contreras enríquez",
    "anthony hernandez": "anthony hernández",
    "anton miranchuk": "anton andreyevich miranchuk",
    "antony": "antony matheus dos santos",
    "anibal godoy": "aníbal cassis godoy lemus",
    "armando cooper": "armando enrique cooper whitaker",
    "artem dzyuba": "artem sergeyevich dzyuba",
    "arthur theate": "arthur nicolas theate",
    "artur jedrzejczyk": "artur jędrzejczyk",
    "ashkan dejagah": "ashkan dejagah",
    "ashley young": "ashley young",
    "assim madibo": "assim omer al haj madibo",
    "awer mabil": "awer bul mabil",
    "axel witsel": "axel witsel",
    "baba rahman": "abdul rahman baba",
    "badou n'diaye": "pape alioune n'diaye",
    "bassam al-rawi": "bassam hisham ali al-rawi",
    "ben white": "benjamin william white",
    "bernardo silva": "bernardo mota veiga de carvalho e silva",
    "brandon aguilera": "brandon aguilera zamora",
    "breel embolo": "breel-donald embolo",
    "bremer": "gleison bremer silva nascimento",
    "brennan johnson": "brennan price johnson",
    "brian idowu": "brian oladapo idowu",
    "bruno alves": "bruno eduardo regufe alves",
    "bruno fernandes": "bruno miguel borges fernandes",
    "bruno guimaraes": "bruno guimarães rodriguez moura",
    "bryan oviedo": "bryan oviedo jiménez",
    "bryan ruiz": "bryan jafet ruiz gonzález",
    "bukayo saka": "bukayo saka",
    "bum-keun song": "bum keun song",
    "cameron devlin": "cameron peter devlin",
    "camilo vargas": "camilo andrés vargas gil",
    "carlos bacca": "carlos arturo bacca ahumada",
    "carlos caceda": "carlos alberto cáceda oyague",
    "carlos martinez": "carlos martínez",
    "carlos pena": "carlos alberto peña rodríguez",
    "carlos sanchez": "carlos alberto sánchez moreno",
    "carlos vela": "carlos alberto vela garrido",
    "casemiro": "carlos henrique casimiro",
    "cassio": "cássio ramos",
    "celso borges": "celso borges mora",
    "chang-hoon kwon": "chang hoon kwon",
    "cheikh n'doye": "cheikh n'doye",
    "chidozie awaziem": "chidozie collins awaziem",
    "christian bassogog": "christian mougang bassogog",
    "christian bolanos": "christian bolaños navarro",
    "christian cueva": "christian alberto cueva bravo",
    "christian ramos": "christian guillermo martín ramos garagay",
    "christian stuani": "christian ricardo stuani curbello",
    "christopher wooh": "christopher maurice wooh",
    "collins fai": "collins ngoran fai",
    "craig goodwin": "craig alexander godwin",
    "cristian ansaldi": "cristian daniel ansaldi",
    "cristian rodriguez": "cristian gabriel rodríguez barotti",
    "cristian romero": "cristian gabriel romero",
    "cristian zapata": "cristián zapata",
    "cyle larin": "cyle christopher larin",
    "cedric soares": "cédric ricardo alves soares",
    "daler kuzyayev": "daler adyamovich kuzyayev",
    "dani alves": "daniel alves da silva",
    "dani carvajal": "daniel carvajal ramos",
    "daniel afriyie": "daniel afriyie barnieh",
    "daniel chacon": "daniel chacón salas",
    "daniel colindres": "daniel colindres solera",
    "danilo": "danilo luiz da silva",
    "danny rose": "daniel lee rose",
    "danny vukovic": "danny vukovic",
    "danny welbeck": "daniel welbeck",
    "david guzman": "david guzmán pérez",
    "david ospina": "david ospina ramírez",
    "david silva": "david josué jiménez silva",
    "david wotherspoon": "david wotherspoon",
    "dayne st. clair": "dayne st. clair",
    "dedryck boyata": "dedryck boyata",
    "dele alli": "bamidele jermaine alli",
    "denis cheryshev": "denis dmitriyevich cheryshev",
    "denis glushakov": "denis borisovich glushakov",
    "denis zakaria": "denis zakaria lako lalo rili",
    "derek cornelius": "derek austin cornelius",
    "devis epassy": "devis rogers epassy mboka",
    "diego laxalt": "diego sebastián laxalt suárez",
    "diego reyes": "diego antonio reyes roales",
    "dimitri petratos": "dimitri petratos",
    "dmitri kombarov": "dmitri vladimirowich kombarov",
    "douglas costa": "douglas costa de souza",
    "douglas lopez": "douglas lópez",
    "eder militao": "éder gabriel militão",
    "edimilson fernandes": "edimilson fernandes ribeiro",
    "edinson cavani": "edinson roberto cavani gómez",
    "edison flores": "edison flores peralta",
    "edson alvarez": "edson omar álvarez velázquez",
    "eduardo salvio": "eduardo antonio salvio",
    "el arabi soudani": "el arbi hillel soudani",
    "el-winsh": "mahmoud hamdy",
    "emil forsberg": "emil peter forsberg",
    "emil krafth": "emil henry kristoffer krafth",
    "eric dier": "eric jeremy edgar dier",
    "erick davis": "erick javier davis grajales",
    "essam el-hadary": "essam el-hadary",
    "esteban alvarado": "esteban alvarado brown",
    "ever banega": "éver maximiliano david banega",
    "everton ribeiro": "éverton augusto de barros ribeiro",
    "exequiel palacios": "exequiel alejandro palacios",
    "fabian schar": "fabian lukas schär",
    "fabinho": "fábio henrique tavares",
    "fabio coentrao": "fábio alexandre da silva coentrão",
    "facundo pellistri": "facundo pellistri rebollo",
    "fagner": "fagner conserva lemos",
    "fahad al-muwallad": "fahad mosaed al-muwallad alhrbi",
    "farid diaz": "farid alfonso díaz rhenals",
    "federico valverde": "federico santiago valverde dipetta",
    "felipe baloy": "felipe abdiel baloy ramírez",
    "fernandinho": "fernando luiz roza",
    "fidel escobar": "fidel escobar mendieta",
    "filip helander": "filip viktor helander",
    "filipe luis": "filipe luís kasmirski",
    "florian thauvin": "florian thauvin",
    "francis uzoho": "francis odinaka uzoho",
    "francisco calvo": "francisco javier calvo quesada",
    "francois moubandje": "françois moubandje",
    "fred": "frederico rodrigues de paula santos",
    "frederik ronnow": "frederik rønnow",
    "frederik schram": "frederik schram",
    "fyodor kudryashov": "fyodor vasilyevich kudryashov",
    "fyodor smolov": "fyodor mikhailovich smolov",
    "gabriel jesus": "gabriel fernando de jesus",
    "gabriel martinelli": "gabriel teodoro martinelli silva",
    "gabriel torres": "gabriel arturo torres tejada",
    "garang kuol": "garang kuol",
    "gareth bale": "gareth frank bale",
    "gary cahill": "gary james cahill",
    "gaston ramirez": "gastón exequiel ramírez pereyra",
    "gaston silva": "gastón alexis silva perdomo",
    "gavi": "pablo martín páez gaviria",
    "gael ondoua": "gaël ondoua",
    "gelson fernandes": "gelson fernandes",
    "gelson martins": "gelson dany batalha martins",
    "gerard pique": "gerard piqué bernabéu",
    "german pezzella": "germán alejo pezzella",
    "gerson torres": "gerson torres barrantes",
    "giancarlo gonzalez": "giancarlo gonzález castro",
    "giorgian de arrascaeta": "giorgian daniel de arrascaeta benedetti",
    "giovani dos santos": "giovani dos santos ramírez",
    "giovanni reyna": "giovanni alejandro reyna",
    "gonzalo montiel": "gonzalo ariel montiel",
    "goncalo guedes": "gonçalo manuel ganchinho guedes",
    "gue-sung cho": "gue sung cho",
    "guillermo ochoa": "francisco guillermo ochoa magaña",
    "gustav svensson": "gustav svensson",
    "gylfi sigurdsson": "gylfi sigurdsson",
    "haitham asiri": "haitham mohammed asiri",
    "harold cummings": "harold cummings",
    "harry maguire": "jacob harry maguire",
    "harry souttar": "harry james souttar",
    "hassan al-haydos": "hassan khalid hassan al-haydos",
    "hassan tambakti": "hassan tambakti",
    "hattan bahebri": "hattan sultan bahebri",
    "hector moreno": "héctor alfredo moreno herrera",
    "heung-min son": "heung min son",
    "hirving lozano": "hirving rodrigo lozano bahena",
    "homam ahmed": "homam al-amin ahmed",
    "hugo ayala": "hugo ayala castro",
    "hyeon-woo jo": "hyeon woo jo",
    "hector herrera": "héctor miguel herrera lópez",
    "hordur magnusson": "hördur magnússon",
    "iago aspas": "iago aspas juncal",
    "ian smith": "ian smith quirós",
    "igor akinfeev": "igor vladimirovich akinfeev",
    "igor smolnikov": "igor alexandrovich smolnikov",
    "ike ugbo": "ike ugbo",
    "ilya kutepov": "ilya olegovich kutepov",
    "in-beom hwang": "in beom hwang",
    "isaac brizuela": "isaac brizuela muñoz",
    "isco": "francisco román alarcón suárez",
    "ismaeel mohammad": "ismaeel mohammad",
    "ismael diaz": "ismael díaz de león",
    "ismael kone": "ismaël koné",
    "jackson irvine": "jackson alexander irvine",
    "jae-sung lee": "jae sung lee",
    "jaime penedo": "jaime manuel penedo cano",
    "james meredith": "james gregory meredith",
    "jamie vardy": "jamie vardy",
    "jan vertonghen": "jan vertonghen",
    "jason cummings": "jason cummings",
    "jassem gaber": "jassem gaber abulsallam",
    "javier aquino": "javier ignacio aquino carmona",
    "javier hernandez": "javier hernández balcázar",
    "javier mascherano": "javier alejandro mascherano",
    "jefferson farfan": "jefferson agustín farfán guadalupe",
    "jefferson lerma": "jefferson andrés lerma solís",
    "jeremy doku": "jérémy doku",
    "jesse lingard": "jesse ellis lingard",
    "jesus gallardo": "jesús daniel gallardo vasconcelos",
    "jewison bennette": "jewison bennette",
    "jimmy durmaz": "jimmy durmaz",
    "joachim andersen": "joachim christian andersen",
    "joel king": "joel bruce king",
    "joel obi": "joel chukwuma obi",
    "joel waterman": "joel waterman",
    "johan mojica": "johan mojica",
    "johan venegas": "johan alberto venegas ulloa",
    "john guidetti": "john alberto guidetti",
    "johnny acosta": "johnny acosta zamora",
    "jonas hector": "jonas hector",
    "jonas hofmann": "jonas hofmann",
    "jonas knudsen": "jonas knudsen",
    "jonas wind": "jonas wind",
    "jonathan david": "jonathan christian david",
    "jonathan urretaviscaya": "jonathan matías urretaviscaya luz luz",
    "jonathan dos santos": "jonathan dos santos ramírez",
    "jong-gyu yoon": "jong gyu yoon",
    "jordan henderson": "jordan brian henderson",
    "jordi alba": "jordi alba ramos",
    "joshua kimmich": "joshua kimmich",
    "jose calderon": "josé calderón frías",
    "jose carvallo": "josé aurelio carvallo alonso",
    "jose fonte": "josé miguel da rocha fonte",
    "jose izquierdo": "josé izquierdo",
    "jose maria gimenez": "josé maría giménez de vargas",
    "joao felix": "joão félix sequeira",
    "joao moutinho": "joão filipe iria santos moutinho",
    "joao mario": "joão mário naval costa eduardo",
    "juan foyth": "juan marcos foyth",
    "juan pablo vargas": "juan pablo vargas campos",
    "juan quintero": "juan fernando quintero paniagua",
    "juan zuniga": "juan camilo zúñiga mosquera",
    "jude bellingham": "jude victor william bellingham",
    "jun-ho son": "jun ho son",
    "jerome boateng": "jérôme boateng",
    "kai havertz": "kai havertz",
    "kamal miller": "kamal miller",
    "kamil glik": "kamil jacek glik",
    "kamil grosicki": "kamil grosicki",
    "kang-in lee": "kang in lee",
    "kara mbodji": "serigne modou kara mbodji",
    "karim adeyemi": "karim david adeyemi",
    "karim benzema": "karim benzema",
    "karim el ahmadi": "karim el ahmadi arrousi",
    "kasper dolberg": "kasper dolberg rasmussen",
    "keanu baccus": "keanu kole baccus",
    "keita balde": "keita baldé diao",
    "kelechi iheanacho": "kelechi promise iheanacho",
    "kendall waston": "kendall jamal waston manley",
    "kenner gutierrez": "kenner gutiérrez cuncas",
    "kenneth omeruo": "kenneth omeruo",
    "kepa arrizabalaga": "kepa arrizabalaga revuelta",
    "keylor navas": "keylor navas gamboa",
    "keysher fuller": "keysher fuller spence",
    "khadim n'diaye": "serigne khadim n'diaye",
    "khalid muneer": "khalid muneer mazeed",
    "khamis al dossari": "khamis al-owairan al-dossari",
    "koke": "jorge resurrección merodio",
    "kye rowles": "kye rowles",
    "kyle walker": "kyle walker",
    "kyung-won kwon": "kyung won kwon",
    "lautaro martinez": "lautaro javier martínez",
    "leandro paredes": "leandro daniel paredes",
    "leon goretzka": "leon goretzka",
    "leonel moreira": "leonel moreira ledesma",
    "leroy sane": "leroy sané",
    "liam fraser": "liam fraser",
    "liam millar": "liam millar",
    "lois openda": "loïs openda",
    "lucas biglia": "lucas rodrigo biglia",
    "lucas cavallini": "lucas daniel cavallini",
    "lucas torreira": "lucas sebastián torreira di pascua",
    "lucas vazquez": "lucas vázquez iglesias",
    "ludwig augustinsson": "hans carl ludwig augustinsson",
    "luis advincula": "luis jan piers advíncula castrillón",
    "luis muriel": "luis fernando muriel fruto",
    "luis ovalle": "luis carlos ovalle victoria",
    "luis tejada": "luis tejada hansell",
    "luiz gustavo": "luiz gustavo dias",
    "lukas klostermann": "lukas klostermann",
    "m'baye niang": "m'baye niang",
    "mahmoud kahraba": "mahmoud abdel-moneim kahraba",
    "majid hosseini": "seyed majid hosseini",
    "mansoor al-harbi": "mansoor ateeq al-harbi",
    "manuel da costa": "manuel marouan da costa trindade senoussi",
    "marcelo gallardo": "marcelo daniel gallardo",
    "marco asensio": "marco asensio willemsen",
    "marco fabian": "marco jhonfai fabián de la mora",
    "marco urena": "marco ureña porras",
    "marcos acuna": "marcos javier acuña",
    "marcos rojo": "marcos alberto rojo",
    "marcus rohden": "marcus rohden",
    "mario martinez": "mario roberto martínez",
    "mark milligan": "mark daniel milligan",
    "marouane fellaini": "marouane fellaini-bakkioui",
    "marquinhos": "marcos aoás corrêa",
    "martin boyle": "martin boyle",
    "martin braithwaite": "martin braithwaite christensen",
    "martin caceres": "josé martín cáceres silva",
    "martin hongla": "martin hongla yma",
    "martin olsson": "martin olsson",
    "martin silva": "martín andrés silva leites",
    "martin campana": "martín nicolás campaña delgado",
    "marwan mohsen": "marwan mohsen",
    "masoud shojaei": "masoud shojaei",
    "massimo luongo": "massimo corey luongo",
    "mateus uribe": "andrés mateus uribe villa",
    "mathew leckie": "mathew leckie",
    "mathew ryan": "mathew david ryan",
    "matthias ginter": "matthias ginter",
    "matias vecino": "matías vecino falero",
    "maximiliano meza": "maximiliano eduardo meza",
    "maximiliano pereira": "victorio maximiliano pereira páez",
    "maxwell": "maxwell scherrer cabelino andrade",
    "medhi benatia": "mehdi benatia",
    "mehdi carcela-gonzalez": "mehdi carcela-gonzález",
    "meshaal barsham": "meshaal aissa barsham",
    "michy batshuayi": "michy batshuayi atunga",
    "miguel araujo": "miguel araujo blanco",
    "miguel borja": "miguel ángel borja hernández",
    "miguel layun": "miguel arturo layún prado",
    "miguel ponce": "miguel ángel ponce briseño",
    "miguel trauco": "miguel ángel trauco saavedra",
    "miguel veloso": "miguel luís pinto veloso",
    "mikael lustig": "mikael lustig",
    "mikkel damsgaard": "mikkel krogh damsgaard",
    "milad mohammadi": "milad mohammadi keshmarzi",
    "mile jedinak": "michael john jedinak",
    "min-jae kim": "min jae kim",
    "min-kyu song": "min kyu song",
    "miranda": "joao miranda de souza filho",
    "mitchell duke": "mitchell thomas duke",
    "mohamed elneny": "mohamed nasser elneny",
    "mohamed kanno": "mohamed kanno",
    "mohamed salah": "mohamed salah hamed mahrous ghaly",
    "mohammad al-sahlawi": "mohammad ibrahim mohammad al-sahlawi",
    "mohammad mazaheri": "mohammad rashid mazaheri",
    "mohammed al rubaie": "mohammed al-rubaie al-yami",
    "moon-hwan kim": "moon hwan kim",
    "mostafa tarek": "mostafa tarek meshaal",
    "motaz hawsawi": "motaz hawsawi",
    "moussa konate": "pape moussa konaté",
    "muhannad assiri": "muhannad ahmed abu radeah assiri",
    "munir el kajoui": "munir mohand mohamedi",
    "musaab khidir": "musaab khidir jabir",
    "mario fernandes": "mario fernandes",
    "mario rui": "mário rui silva duarte",
    "n'golo kante": "n'golo kanté",
    "nacho": "josé ignacio fernández iglesias",
    "nacho monreal": "ignacio monreal eraso",
    "nahitan nandez": "nahitan michel nández acosta",
    "nahuel guzman": "nahuel ignacio guzmán",
    "nahuel molina": "nahuel molina lucero",
    "naif al-hadhrami": "naif abdulraheem al-hadhrami",
    "nani": "luís carlos almeida da cunha",
    "nasser al-dawsari": "nasser eissa shafi al-dawsari",
    "nawaf al-abed": "nawaf shaker al-abed",
    "nawaf al-aqidi": "nawaf dhahi faisal al-suwaiti al-aqidi",
    "neto": "norberto murara neto",
    "nick pope": "nicholas david pope",
    "nicolas lodeiro": "marcelo nicolás lodeiro benítez",
    "nicolas ngamaleu": "nicolas moumi ngamaleu",
    "nicolas otamendi": "nicolás hernán otamendi",
    "nicolas tagliafico": "nicolás alejandro tagliafico",
    "nikita rukavytsya": "nikita vadymovych rukavytsya",
    "nilson loyola": "nilson loyola morales",
    "nyom": "allan-roméo nyom",
    "odion ighalo": "odion jude ighalo",
    "ogenyi onazi": "ogenyi onazi",
    "oghenekaro etebo": "oghenekaro etebo",
    "ola toivonen": "nils ola toivonen",
    "olivier mbaizo": "olivier mbaissidara mbaizo",
    "olivier ntcham": "olivier ntcham",
    "omar gaber": "omar gaber",
    "omid ebrahimi": "omid ebrahimi",
    "oribe peralta": "oribe peralta morones",
    "oscar boniek garcia": "oscar boniek garcía",
    "ousmane viera": "ousmane viera diarrassouba",
    "paolo guerrero": "josé paolo guerrero gonzales",
    "paolo hurtado": "paolo hurtado",
    "patrick pemberton": "patrick pemberton bernard",
    "patrick sequeira": "patrick sequeira",
    "paulo dybala": "paulo bruno dybala",
    "pedri": "pedro gonzález lópez",
    "pedro aquino": "pedro jesús aquino sánchez",
    "pedro gallese": "pedro gallese",
    "pedro geromel": "pedro tonon geromel",
    "pedro miguel": "pedro miguel carvalho deus correia",
    "pepe reina": "josé manuel reina páez",
    "pierre kunde": "pierre kunde malong",
    "pierre-emile hojbjerg": "pierre-emile højbjerg",
    "pione sisto": "pione sisto ifolo emy emirmija",
    "piotr zielinski": "piotr sebastian zieliński",
    "radamel falcao": "radamel falcao garcía zárate",
    "rafa": "rafael alexandre fernandes ferreira silva",
    "rafael marquez": "rafael márquez álvarez",
    "raheem sterling": "raheem shaquille sterling",
    "rais m'bolhi": "Rais M'Bolhi",
    "ramadan sobhi": "ramadan sobhi ahmed",
    "randall azofeifa": "randall azofeifa corrales",
    "raphael guerreiro": "raphaël adelino josé guerreiro",
    "rasmus kristensen": "rasmus nissen kristensen",
    "raul meireles": "raul josé trinas meireles",
    "raul jimenez": "raúl alonso jiménez rodríguez",
    "raul ruidiaz": "raúl mario ruidíaz misitich",
    "renato augusto": "renato augusto",
    "renato tapia": "renato tapia",
    "reza ghoochannejhad": "reza ghoochannejhad",
    "ricardo pereira": "ricardo pereira",
    "ricardo quaresma": "ricardo quaresma",
    "ricardo rodriguez": "ricardo rodríguez araya",
    "richarlison": "richarlison de andrade",
    "riley mcgree": "riley mcgree",
    "riyadh sharahili": "riyadh sharahili",
    "robbie kruse": "robbie thomas kruse",
    "roberto firmino": "roberto firmino barbosa de oliveira",
    "rodrigo bentancur": "rodrigo bentancur colmán",
    "rodrigo de paul": "rodrigo javier de paul",
    "rodrigo moreno": "rodrigo moreno machado",
    "rodrygo": "rodrygo silva de goes",
    "romain saiss": "romain saïss",
    "roman zobnin": "roman sergeyevich zobnin",
    "roman torres": "román torres rodríguez",
    "rony martinez": "rony martínez",
    "ruben amorim": "rúben filipe marques amorim",
    "rubin colwill": "rubin colwill",
    "rui patricio": "rui pedro dos santos patrício",
    "ronald matarrita": "ronald matarrita ulate",
    "saad al sheeb": "saad abdullah al-sheeb",
    "saad samir": "saad samir",
    "saeid ezatolahi": "saeid ezatolahi afagh",
    "salem al-dawsari": "salem muhamed al-dawsari",
    "salem al-hajri": "salem ali salem al-hajri",
    "salman al-faraj": "salman mohammed al-faraj",
    "sam morsy": "samy sayed morsy",
    "sammir": "jorge sammir cruz campos",
    "samuel umtiti": "samuel umtiti",
    "samuel fridjonsson": "samúel fridjónsson",
    "sang-ho na": "sang ho na",
    "santiago arias": "santiago arias naranjo",
    "saud abdulhamid": "saud abdullah abdulhamid",
    "saul niguez": "saúl ñíguez esclápez",
    "sebastian larsson": "sebastian larsson",
    "serge gnabry": "serge gnabry",
    "sergei ignashevich": "sergei nikolayevich ignashevich",
    "sergio aguero": "sergio leonel agüero del castillo",
    "sergio busquets": "sergio busquets i burgos",
    "seung-ho paik": "seung ho paik",
    "sherif ekramy": "sherif ekramy ahmed ahmed el-shahat",
    "shikabala": "mahmoud abdel razek fadlallah",
    "simeon nwankwo": "simy",
    "simon mignolet": "simon mignolet",
    "stephen eustaquio": "stephen eustáquio",
    "steven gerrard": "steven gerrard",
    "steven nzonzi": "steven n'kemboanza mike christopher nzonzi",
    "steven vitoria": "steven de sousa vitória",
    "sultan al-ghanam": "sultan abdullah al-ghanam",
    "sławomir peszko": "sławomir konrad peszko",
    "tae-hwan kim": "tae hwan kim",
    "taison": "taison barcellos freda",
    "tajon buchanan": "tajon trevor buchanan",
    "thiago almada": "thiago ezequiel almada",
    "thiago cionek": "thiago rangel cionek",
    "thomas delaney": "thomas delaney",
    "thomas deng": "thomas deng",
    "thorgan hazard": "thorgan hazard",
    "tim cahill": "timothy joel cahill",
    "toby alderweireld": "tobias albertine maurits alderweireld",
    "tom rogic": "tomas petar rogic",
    "trent sainsbury": "trent lucas sainsbury",
    "trezeguet": "mahmoud ibrahim hassan",
    "ui-jo hwang": "ui jo hwang",
    "victor lindelof": "victor jörgen nilsson lindelöf",
    "victor nelsson": "victor enok nelsson",
    "viktor claesson": "viktor claesson",
    "viktor fischer": "viktor fischer",
    "vincent kompany": "vincent kompany",
    "vinicius junior": "vinícius josé paixão de oliveira júnior",
    "vladimir gabulov": "vladimir borisovich gabulov",
    "vladimir granat": "vladimir vasilyevich granat",
    "wayne rooney": "wayne rooney",
    "weverton": "weverton pereira da silva",
    "wilder cartagena": "wilder cartagena",
    "wilfred ndidi": "onyinye wilfred ndidi",
    "wilfredo caballero": "wilfredo daniel caballero lazcano",
    "william carvalho": "william silva de carvalho",
    "william kvist": "william kvist jørgensen",
    "willian": "willian borges da silva",
    "wojciech szczesny": "wojciech tomasz szczęsny",
    "woo-yeong jeong": "woo yeong jeong",
    "wilmar barrios": "wílmar enrique barrios terán",
    "yahya al-shehri": "yahya sulaiman ali al-shehri",
    "yannick carrasco": "yannick ferreira carrasco",
    "yasser al-mosailem": "yasser abdullah al-mosailem",
    "yasser al-shahrani": "yasser gharsan al-shahrani",
    "yeltsin tejeda": "yeltsin tejeda valverde",
    "yerry mina": "yerry fernando mina gonzález",
    "yoshimar yotun": "victor yoshimar yotún flores",
    "youstin salas": "youstin delfín salas gómez",
    "yu-min cho": "Cho Yu-min",
    "yuri zhirkov": "yuri valentinovich zhirkov",
    "yvon mvogo": "yvon landry mvogo nganoma",
    "zeno debast": "zeno koen debast",
    "alvaro morata": "álvaro borja morata martín",
    "alvaro odriozola": "álvaro odriozola arzallus",
    "alvaro zamora": "álvaro jose zamora",
    "angel correa": "ángel martín correa martínez",
    "edgar joel barcenas": "édgar joel bárcenas herrera",
    "erick gutierrez": "erick gabriel gutiérrez galaviz",
    "oscar duarte": "oscar duarte gaitán",
    "oscar murillo": "óscar fabián murillo murillo",
    "xabi alonso" : "xabier alonso olano",
    "woo-yeong jeong" : "jeong woo-yeong",
    "william kvist" : "william vitved kvist",
    "wilder cartagena" : "wilder josé cartagena mendoza",
    "wayne rooney" : "Wayne Mark Rooney",
    "vincent kompany" : "vincent jean mpoy kompany",
    "viktor fischer" : "viktor gorridsen fischer",
    "viktor claesson" : "viktor johan anton claesson",
    "ui-jo hwang" : "hwang ui-jo",
    "tim cahill" : "timothy filiga cahill",
    "thorgan hazard" : "thorgan ganael francis hazard",
    "thomas deng" : "thomas jok deng",
    "thomas delaney" : "thomas joseph delaney",
    "tae-hwan kim" : "kim tae-hwan",
    "steven gerrard" : "steven george gerrard",
    "stephen eustaquio" : "stephen antunes eustáquio",
    "simon mignolet" : "simon luc hildebert mignolet",
    "simeon nwankwo" : "simeon tochukwu nwankwo",
    "seung-ho paik" : "paik seung-ho",
    "serge gnabry" : "serge david gnabry",
    "segundo castillo" : "segundo alejandro castillo",
    "sebastian larsson" : "sebastian bengt ulf larsson",
    "sang-ho na" : "na sang-ho",
    "samuel fridjonsson" : "samúel kári friðjónsson",
    "samuel umtiti" : "samuel yves umtiti",
    "saad samir" : "saad el-din samir",
    "ronald matarrita" : "rónald alberto matarrita ulate",
    "rubin colwill" : "rubin james colwill",
    "rony martinez" : "rony darío martínez alméndarez",
    "roman torres" : "román aureliano torres morcillo",
    "romain saiss" : "romain ghanem paul saïss",
    "rolando irusta" : "rolando hugo irusta",
    "roberto sosa" : "roberto eliseo sosa",
    "riyadh sharahili" : "riyadh mohammed sharahili",
    "riley mcgree" : "riley patrick mcGree",
    "ricardo quaresma" : "ricardo andrade quaresma bernardo",
    "ricardo pereira" : "ricardo domingos barbosa pereira",
    "ricardo costa" : "ricardo miguel moreira da costa",
    "reza ghoochannejhad" : "reza ghoochannejhad nournia",
    "renato tapia" : "renato fabrizio tapia cortijo",
    "renato augusto" : "renato soares de oliveira augusto",
    "ramadan sobhi" : "ramadan sobhi ramadan ahmed",
    "rais m'bolhi" : "rais m'bolhi",
    "pedro gallese" : "pedro david gallese quiroz",
    "paulo dybala" : "paulo exequiel dybala",
    "patrick sequeira" : "patrick gilmar sequeira mejías",
    "paolo hurtado" : "cristopher paolo césar hurtado huertas",
    "oscar boniek garcia" : "óscar boniek garcía ramírez",
    "omid ebrahimi" : "omid ebrahimi zarandini",
    "omar gaber" : "omar mahmoud gabe",
    "olivier ntcham" : "jules olivier ntcham",
    "oghenekaro etebo" : "etebo peter oghenekaro",
    "ogenyi onazi" : "ogenyi eddy onazi",
    "neto" : "rodrigues neto",
    "nahuel guzman" : "nahuel ignacio guzmán palomeque",
    "n'golo kante" : "n''golo kanté",
    "mario fernandes" : "mário figueira fernandes",
    "musaab khidir" : "musaab khidir kamal mohamed",
    "munir el kajoui" : "munir mohand mohamedi el kajoui",
    "motaz hawsawi" : "motaz ali hassan hawsawi",
    "moon-hwan kim" : "kim moon-hwan",
    "mohamed kanno" : "mohamed ibrahim kanno",
    "mohamed elneny" : "mohamed naser elsayed elneny",
    "min-kyu song" : "song min-kyu",
    "min-jae kim" : "kim min-jae",
    "mikael lustig" : "carl mikael lustig",
    "miguel ponce" : "miguel ángel ponce",
    "mehdi carcela-gonzalez" : "mehdi françois carcela-gonzález",
    "medhi benatia" : "medhi amine el mouttaqi benatia",
    "matthias ginter" : "matthias lukas ginter",
    "mathew leckie" : "mathew allan leckie",
    "masoud shojaei" : "masoud soleimani shojaei",
    "marwan mohsen" : "marwan mohsen fahmi tharwat",
    "martin olsson" : "martin tony waikwa olsson",
    "martin o'neill" : "martin o''neill",
    "martin boyle" : "martin callie boyle",
    "mario perez" : "mario pérez guadarrama",
    "mario martinez" : "mario roberto martínez hernández",
    "marcus rohden" : "marcus christer rohdén",
    "marcos rojo" : "faustino marcos alberto rojo",
    "marco urena" : "marco danilo ureña porras",
    "marcelino" : "marcelino cargas",
    "manuel sanchis" : "manuel sanchís martínez",
    "manuel jimenez" : "manuel jiménez jiménez",
    "mahmoud kahraba" : "mahmoud abdel-moneim",
    "m'baye niang" : "m''baye babacar niang",
    "lukas klostermann" : "lukas manuel klostermann",
    "luis tejada" : "luis carlos tejada hansell",
    "luis perez" : "luis ernesto pérez gómez",
    "luis lopez" : "luis aurelio lópez fernández",
    "lois openda" : "ikoma loïs openda",
    "liam millar" : "liam alan millar",
    "liam fraser" : "liam scott fraser",
    "leroy sane" : "leroy aziz sané",
    "leonel moreira" : "leonel gerardo moreira ledezma",
    "leon goretzka" : "leon christoph goretzka",
    "laurent ciman" : "laurent franco ciman",
    "landry n'guemo" : "landry n''guémo",
    "kyung-won kwon" : "kwon kyung-won",
    "kyle walker" : "kyle andrew walker",
    "kye rowles" : "kye francis rowles",
    "khalid muneer" : "khalid muneer ali abu bakr mazeed",
    "khadim n'diaye" : "serigne khadim n''diaye",
    "keylor navas" : "keylor antonio navas gamboa",
    "kenneth omeruo" : "kenneth josiah omeruo",
    "karim benzema" : "karim mostafa benzema",
    "kang-in lee" : "lee kang-in",
    "kamil grosicki" : "kamil paweł grosicki",
    "kamal miller" : "kamal anthony miller",
    "kaka" : "ricardo izecson dos santos leite",
    "kai havertz" : "kai lukas havertz",
    "jerome boateng" : "jérôme agyenim boateng",
    "jun-ho son" : "son jun-ho",
    "jose izquierdo" : "josé heriberto izquierdo mena",
    "jose holebas" : "josé lIoyd holebas",
    "jose calderon" : "josé de jesus calderón fria",
    "joshua kimmich" : "joshua walter kimmich",
    "jorge nunez" : "jorge martín núñez mendoza",
    "jong-gyu yoon" : "yoon jong-gyu",
    "jonas wind" : "jonas older wind",
    "jonas knudsen" : "jonas hjort knudsen",
    "jonas hofmann" : "jonas hofmann (heidelberg",
    "jonas hector" : "jonas armin hector",
    "johnny van 't schip" : "johnny van ''t schip",
    "john o'neill" : "john o''neill",
    "john o'brien" : "john o''brien",
    "johan mojica" : "johan andrés mojica palacio",
    "johan djourou" : "johan danon djourou-gbadjere",
    "joel waterman" : "joel robert waterman",
    "joao pinto" : "joão manuel vieira pinto",
    "jo" : "poong jo kim",
    "jimmy durmaz" : "jakup jimmy durmaz",
    "jewison bennette" : "jewison francisco bennette villegas",
    "andrei semionov" : "andrei sergeyevich semyonov",
    "andy o'brien" : "andy o''brien",
    "anthony hernandez" : "anthony william hernández gonzález",
    "anibal godoy" : "aníbal cesis godoy",
    "ari skulason" : "ari freyr skúlason",
    "aron gunnarsson" : "aron einar malmquist gunnarsson",
    "artur jedrzejczyk" : "artur martin jędrzejczyk",
    "arturo vidal" : "arturo erasmo vidal pardo",
    "ashkan dejagah" : "seyed ashkan dejagah",
    "ashley young" : "ashley simon young",
    "axel witsel" : "axel laurent angel lambert witsel",
    "bernard" : "bernard anício caldeira duarte",
    "bjorn sigurðarson" : "björn bergmann sigurðarson",
    "blas perez" : "blas antonio miguel pérez ortega",
    "bukayo saka" : "bukayo ayoyinka temidayo saka",
    "bum-keun song" : "song bum-keun",
    "carlos martinez" : "carlos manuel martínez castro",
    "carlos tevez" : "carlos alberto martínez tevez",
    "carlos valderrama" : "carlos alberto valderrama palacio",
    "chang-hoon kwon" : "kwon chang-hoon",
    "cheikh n'doye" : "cheikh n''doye",
    "cristian zapata" : "cristián eduardo zapata valencia",
    "daniel chacon" : "daniel alonso chacón salas",
    "danny vukovic" : "daniel vukovic",
    "danny welbeck" : "daniel nii tackie mensah welbeck",
    "dante" : "dante bonfim",
    "david beckham" : "david robert joseph beckham",
    "david guzman" : "david alberto guzmán pérez",
    "david o'leary" : "david o''leary",
    "david wotherspoon" : "david wallace wotherspoon",
    "dayne st. clair" : "dayne tristan st. clair",
    "dedryck boyata" : "anga dedryck boyata",
    "denis zakaria" : "denis lemi zakaria lako lado",
    "didier drogba" : "didier yves drogba tébily",
    "diego perez" : "diego fernando pérez aguado",
    "dimitri petratos" : "dimitri ''dimi'' petratos",
    "dobromir zhechev" : "dobromir georgiev zhechev",
    "douglas lopez" : "douglas andrey lópez araya",
    "edison flores" : "edison michael flores peralta",
    "eduardo" : "eduardo nino",
    "enzo francescoli" : "enzo francescoli uriarte",
    "ermindo onega" : "ermindo ángel onega",
    "essam el-hadary" : "essam kamal tawfiq el-hadary",
    "fabian o'neill" : "fabian o''neill",
    "faustino asprilla" : "faustino hernán asprilla hinestroza",
    "fernando gago" : "fernando rubén gago",
    "florian thauvin" : "florian tristan mariano thauvin",
    "francois moubandje" : "jacques françois moubandje",
    "frederik schram" : "frederik august albrecht schram",
    "garang kuol" : "farang mawien kuol",
    "gael ondoua" : "gaël bella ondoua",
    "gelson fernandes" : "gelson da conceição tavares fernandes",
    "goikoetxea" : "andoni goikoetxea olaskoaga",
    "gonzalo higuain" : "gonzalo gerardo higuaín",
    "gue-sung cho" : "cho gue-sung",
    "gustav svensson" : "karl gustav johan svensson",
    "gylfi sigurdsson" : "gylfi pór sigurðsson",
    "harold cummings" : "harold oshkaly cmmings segura",
    "hassan tambakti" : "hassan mohammed tambakti",
    "hector ortiz" : "héctor ortiz benítez",
    "helder postiga" : "hélder manuel marques postiga",
    "henrique" : "carlos henrique casimiro",
    "hernanes" : "anderson hernanes de carvalho andrade lima",
    "heung-min son" : "son heung-min",
    "hugo sanchez" : "hugo sánchez márquez",
    "hulk" : "givanildo vieira de souza",
    "alfredo di Stefano" : "alfredo stéfano di stéfano laulhé",
    "hyeon-woo jo" : "jo hyeon-woo",
    "hordur magnusson" : "hörður björgvin magnússon",
    "ignacio ambriz" : "marcos ignacio ambriz espinoza",
    "ike ugbo" : "iké dominique ugbo",
    "in-beom hwang" : "hwang in-beom",
    "ismaeel mohammad" : "ismaeel mohammad mohammad",
    "ismael kone" : "ismaël kenneth jordan koné",
    "jae-sung lee" : "lee jae-sung",
    "jamie vardy" : "jmie richard vardy",
    "jan vertonghen" : "jan bert lieve vertonghen",
    "jason cummings" : "jason steven cummings",
    "jeremy doku" : "jérémy baffour doku",
    "jerry palacios" : "jerry nelson palacios suazo",
    "john o'brien" : "john o''brien",
    "john o'neill" : "john o''neill",
    "johnny van 't schip" : "johnny van ''t schip",
    "juanfran" : "juanfran torres",
    "juanito" : "Juan"
}


# ─────────────────────────────────────────────
#  UTILIDADES
# ─────────────────────────────────────────────
def normalizar(texto):
    texto = texto.strip()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", texto).lower()


def log(msg):
    print(msg)


# ─────────────────────────────────────────────
#  CARGA DE MAPPINGS DESDE SQL
# ─────────────────────────────────────────────
def cargar_paises():
    """Retorna {nombre_exacto: id_pais}"""
    mapa    = {}
    pattern = re.compile(r"VALUES\s*\(\s*(\d+),\s*'([^']*(?:''[^']*)*)'", re.I)
    with open(PAIS_SQL, encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if "INSERT INTO Pais" not in linea:
                continue
            m = pattern.search(linea)
            if m:
                id_pa  = int(m.group(1))
                nombre = m.group(2).replace("''", "'")
                if nombre not in mapa:
                    mapa[nombre] = id_pa
    log(f"[DEBUG] Paises cargados: {len(mapa)}")
    return mapa


def cargar_jugadores():
    """Retorna {nombre_norm: id_jugador}"""
    jugadores = {}
    patron    = re.compile(r"VALUES\s*\((\d+),\s*'([^']*)'")
    with open(JUGADOR_SQL, encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if "INSERT INTO Jugador" not in linea and "INSERT INTO jugador" not in linea:
                continue
            m = patron.search(linea)
            if m:
                id_ju  = int(m.group(1))
                nombre = m.group(2).replace("''", "'")
                key    = normalizar(nombre)
                if key not in jugadores:
                    jugadores[key] = id_ju
    log(f"[DEBUG] Jugadores cargados: {len(jugadores)}")
    return jugadores


# ─────────────────────────────────────────────
#  RESOLUCIÓN DE ENTIDADES
# ─────────────────────────────────────────────
def buscar_pais_id(nombre_html, paises):
    """Alias -> exacto -> sin acentos. Retorna id o None."""
    nombre = PAIS_ALIAS.get(nombre_html, nombre_html)
    if nombre in paises:
        return paises[nombre]
    norm = normalizar(nombre)
    for nombre_sql, id_pa in paises.items():
        if normalizar(nombre_sql) == norm:
            return id_pa
    return None


def buscar_jugador_id(nombre_html, jugadores, umbral=0.85):
    """
    Resuelve id_jugador en 4 niveles:
      1. Alias con ID directo
      2. Alias con nombre SQL
      3. Búsqueda exacta normalizada
      4. Fuzzy matching con difflib
    """
    norm = normalizar(nombre_html)

    # 1. Buscar en ALIAS_JUGADORES
    alias_val = ALIAS_JUGADORES.get(norm) or ALIAS_JUGADORES.get(nombre_html)

    if alias_val is not None:
        # 1a. Alias es ID directo
        if isinstance(alias_val, int):
            log(f"  [ALIAS-ID]  '{nombre_html}' -> id={alias_val}")
            return alias_val
        # 1b. Alias es nombre completo
        norm_alias = normalizar(alias_val)
        if norm_alias in jugadores:
            log(f"  [ALIAS-NOM] '{nombre_html}' -> '{alias_val}' -> id={jugadores[norm_alias]}")
            return jugadores[norm_alias]
        norm = norm_alias  # continuar fuzzy con el nombre del alias

    # 2. Exacto normalizado
    if norm in jugadores:
        log(f"  [EXACT]     '{nombre_html}' -> id={jugadores[norm]}")
        return jugadores[norm]

    # 3. Fuzzy matching
    candidatos = difflib.get_close_matches(norm, list(jugadores.keys()), n=1, cutoff=umbral)
    if candidatos:
        mejor = candidatos[0]
        log(f"  [FUZZY]     '{nombre_html}' -> '{mejor}' -> id={jugadores[mejor]}")
        return jugadores[mejor]

    log(f"  [ERROR]     Jugador no encontrado: '{nombre_html}'")
    return None


# ─────────────────────────────────────────────
#  PARSEO DEL HTML
# ─────────────────────────────────────────────
def extraer_datos_partido(filepath):
    """
    Parsea un HTML de partido y retorna lista de dicts por equipo.
    Extrae: pais, entrenador, y por cada jugador:
      nombre, posicion (AR/DF/MC/DL), camiseta, capitan, titular
    """
    resultado = []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    h3 = soup.find("h3", string=re.compile(r"Jugadores", re.I))
    if not h3:
        return resultado

    container = h3.find_next("div", class_="clearfix")
    if not container:
        return resultado

    for tabla in container.find_all("table", class_="a-center"):
        pais       = None
        entrenador = None
        jugadores  = []

        # ── País ──
        td_pais = tabla.find("td", style=re.compile(r"height:\s*40px"))
        if td_pais:
            img = td_pais.find("img", alt=True)
            if img:
                pais = img["alt"].strip()
        if not pais:
            continue

        # ── Entrenador ──
        for td in tabla.find_all("td"):
            strong = td.find("strong")
            if strong and "Entrenador:" in strong.get_text():
                entrenador = td.get_text().split("Entrenador:")[-1].strip()
                break

        # ── Jugadores ──
        es_titular = True

        for tr in tabla.find_all("tr"):
            texto_tr = tr.get_text().strip().lower()

            if "titulares" in texto_tr and len(tr.find_all("td")) <= 3:
                es_titular = True
                continue
            if "suplentes" in texto_tr and len(tr.find_all("td")) <= 3:
                es_titular = False
                continue

            if "a-top" not in tr.get("class", []):
                continue

            tds = tr.find_all("td")
            if len(tds) < 3:
                continue

            posicion = tds[0].get_text(strip=True).upper()
            if posicion not in ("AR", "DF", "MC", "DL"):
                continue

            try:
                no_camiseta = int(tds[1].get_text(strip=True))
            except ValueError:
                no_camiseta = None

            td_jug = tds[2]
            link   = td_jug.find("a", href=re.compile(r"jugadores/"))
            if not link:
                continue

            nombre_jug = link.get_text(strip=True)
            div_left   = td_jug.find("div", class_="left")
            texto_div  = div_left.get_text() if div_left else ""
            es_capitan = 1 if "(C)" in texto_div else 0

            jugadores.append({
                "nombre"   : nombre_jug,
                "posicion" : posicion,
                "camiseta" : no_camiseta,
                "capitan"  : es_capitan,
                "titular"  : 1 if es_titular else 0,
            })

        if jugadores:
            resultado.append({
                "pais"       : pais,
                "entrenador" : entrenador or "",
                "jugadores"  : jugadores,
            })

    return resultado


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    log("=" * 65)
    log("SCRAPER PLANTILLA + POSICION_JUGADOR")
    log("=" * 65)

    paises    = cargar_paises()
    jugadores = cargar_jugadores()

    plantillas_map    = {}
    next_id_pla       = 1
    posiciones_lista  = []
    posiciones_vistas = set()
    sin_match_pais    = set()
    sin_match_jugador = set()

    year_dirs = sorted([
        d for d in HTML_DIR.iterdir()
        if d.is_dir() and d.name.isdigit()
    ])

    total_html = 0
    for year_dir in year_dirs:
        html_files  = list(year_dir.glob("*.html"))
        total_html += len(html_files)
        log(f"\n[AÑO {year_dir.name}] {len(html_files)} archivos")

        for html_file in html_files:
            equipos = extraer_datos_partido(html_file)

            for equipo in equipos:
                pais_id = buscar_pais_id(equipo["pais"], paises)
                if pais_id is None:
                    sin_match_pais.add(equipo["pais"])
                    continue

                clave_pla = (pais_id, equipo["entrenador"])
                if clave_pla not in plantillas_map:
                    plantillas_map[clave_pla] = next_id_pla
                    next_id_pla += 1
                id_pla_prov = plantillas_map[clave_pla]

                for jug in equipo["jugadores"]:
                    jugador_id = buscar_jugador_id(jug["nombre"], jugadores)
                    if jugador_id is None:
                        sin_match_jugador.add(jug["nombre"])
                        continue

                    clave_pos = (id_pla_prov, jugador_id)
                    if clave_pos in posiciones_vistas:
                        continue
                    posiciones_vistas.add(clave_pos)

                    posiciones_lista.append({
                        "id_pla_prov" : id_pla_prov,
                        "id_ju"       : jugador_id,
                        "posicion"    : jug["posicion"],
                        "capitan"     : jug["capitan"],
                        "camiseta"    : jug["camiseta"],
                        "titular"     : jug["titular"],
                    })

    # ── Reporte en consola ──
    log(f"\n{'='*65}")
    log(f"Total HTML procesados        : {total_html}")
    log(f"Plantillas únicas            : {len(plantillas_map)}")
    log(f"Registros Posicion_Jugador   : {len(posiciones_lista)}")

    if sin_match_pais:
        log(f"\n[WARN] Paises sin resolver ({len(sin_match_pais)}):")
        for p in sorted(sin_match_pais):
            log(f"  - {p}")

    if sin_match_jugador:
        log(f"\n[WARN] Jugadores sin resolver ({len(sin_match_jugador)}):")
        for j in sorted(sin_match_jugador):
            log(f"  - {j}")

        # ── Escribir jugadores_no_encontrados.txt ──
        with open(OUT_NO_ENCONTRADOS, "w", encoding="utf-8") as f:
            for j in sorted(sin_match_jugador):
                f.write(f"{normalizar(j)}\n")


        log(f"\n[OK] No encontrados  -> {OUT_NO_ENCONTRADOS.absolute()}")

    # ── Ordenar plantillas por (pais_id, entrenador) ──
    plantillas_sorted = sorted(plantillas_map.items(), key=lambda x: (x[0][0], x[0][1]))

    # Remapear id provisional -> id final secuencial
    remap_id_pla = {
        id_prov: i
        for i, ((_, _), id_prov) in enumerate(plantillas_sorted, 1)
    }

    # ── Generar 10plantilla.sql ──
    with open(OUT_PLANTILLA, "w", encoding="utf-8") as f:
        f.write("-- 10plantilla.sql  -  generado automaticamente\n")
        f.write(f"-- Fecha  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total  : {len(plantillas_sorted)} registros\n\n")

        for i, ((pais_id, entrenador), _) in enumerate(plantillas_sorted, 1):
            ent_esc = entrenador.replace("'", "''")
            f.write(
                f"INSERT INTO Plantilla (id_pla, Pais_id_pa, director_tecnico_pla) "
                f"VALUES ({i}, {pais_id}, '{ent_esc}');\n"
            )

    log(f"[OK] Plantilla       -> {OUT_PLANTILLA.absolute()}")

    # ── Generar 18posicionjugador.sql ──
    with open(OUT_POSICION, "w", encoding="utf-8") as f:
        f.write("-- 18posicionjugador.sql  -  generado automaticamente\n")
        f.write(f"-- Fecha  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total  : {len(posiciones_lista)} registros\n")
        f.write("-- Requiere que 10plantilla.sql se haya ejecutado antes\n\n")

        for pos in posiciones_lista:
            id_pla_final = remap_id_pla[pos["id_pla_prov"]]
            camiseta_val = str(pos["camiseta"]) if pos["camiseta"] is not None else "NULL"

            f.write(
                f"INSERT INTO Posicion_Jugador "
                f"(Plantilla_id_pla, Jugador_id_ju, nombre_po_ju, capitan, no_camiseta, titular) "
                f"VALUES ({id_pla_final}, {pos['id_ju']}, "
                f"'{pos['posicion']}', {pos['capitan']}, {camiseta_val}, {pos['titular']});\n"
            )

    log(f"[OK] Posicion Jugador-> {OUT_POSICION.absolute()}")
    log("=" * 65)


if __name__ == "__main__":
    main()
