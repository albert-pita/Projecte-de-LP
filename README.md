# Projecte-de-LP
Projecte de LP - QuizBot - Edició tardor 2019/20

Aquest és el projecte per l'assignatura GEI-LP (edicio tardor 2019). Consisteix en un chatbot que permet recollir les dades d'enquestes definides mitjançant un compilador a través de telegram i poder fer sobre les dades recollides d'aquestes consultes gràfiques simples i informes.

## Getting Started

Aquestes instruccions us proporcionaran una còpia del projecte en funcionament a la vostra màquina local amb finalitats de desenvolupament i proves. Consulteu les notes per saber com obrir el projecte al vostre sistema.

### Prerequisites

Abans de posar en funcionament el projecte és necessita instal·lar:

```
pip install -r requirements.txt
```
Aquest són els requeriments per tot el codi.
També peró s'ha d'instal·lar ANTLR4. Per fer-ho has de:
 - Descarregar el ANTLR4.jar file:

* [jar file](https://www.antlr.org/download/antlr-4.7.1-complete.jar)
* [Getting started](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)

 - Install python runtime:

```
pip install antlr4-python3-runtime

or

pip install antlr4-python3-runtime
```

### Running

A la primera part del projecte s'havia de realitzar un compilador que interpretés un llenguatge Enquestes de definicio d'enquestes.
Es demanava que es fes una certa gramatica per aquest llenguatge i que es passes una enquesta en format AST a un graf. Per poder compilar
i executar aixo s'ha de fer el seguent:

Primer de tot s'ha de compilar la gramàtica Enquestes.g amb ANTLR4.

```
antlr4 -Dlanguage=Python3 -no-listener -visitor Enquestes.g
```

El visitor que ens crea aquesta comanda no és el que volem, aixi que s'ha de canviar pel visitor test.EnquestesVisitor.py.
El canvi el podem fer mitjançant la comanda si s'esta utilitzant Linux:

```
cp test.EnquestesVisitor.py EnquestesVisitor.py
```

O copiar el contingut fent copiant i enganxant si s'esta utilitzant Windows.
Per poder utilitzar-ho, s'ha d'executar l'script passant-li també l'enquesta, en aquest cas l'arxiu test.txt:

```
python test.script.py test.txt
```

Quan s'hagi executat se'ns mostrara una imatge del graf de l'enquesta i tambe a la carpeta s'haura generat un .png amb aquesta.

A la segona part del projecte s'havia de realtizar un bot per telegram que pogues contestar textualment i graficament a preguntes relaciondes amb una enquesta i recollir les dades obtingudes. Per poder utilitzar aquesta part es recomana juntar les dues carpetes, bot i cl, en una ja que hi han arxius necessaris pel bot que es generen amb el script del compilador. En cas que no es vulguin juntar, nomes passeu els arxius graph.pkl i resKeeper.pkl a la carpeta bot.

Per posar en marxa el bot simplement s'ha de fer, tenint previament un fitxer amb un cert token donat per @BotFather:

```
python3 bot.py
```

Un cop executat el bot estara actiu. Si es va a l'aplicacio Telegram i es busca @ClassicSurveyorBot el trobara, es diu Wilson, y ja pot interactuar amb ell.

### Functioning

El funcionament del bot es bastant senzill i es poden utilitzar totes les comandes descrites a l'enunciat de la practica. Tot i aixi te algunes excepcions
i alguns temes que cal puntualitzar.

Quan es vol crear mes d'una enquesta, les quals tenen id diferents, es pot fer, l'unic que aquestes no poden tenir preguntes o nodes comuns ja que sino el bot
podra confondre les dues enquestes i escriure preguntes que no toquen.

El bot assumeix tambe que les respostes donades pels enquestats son correctes, referint-se a que estan escollint una de les opcions presentades.

## Built With

* [Python](https://docs.python.org/3/) - Llenguatge utilitzat
* [Telegram](https://core.telegram.org/bots) - Aplicació on funciona el bot
* [Matplotlib](https://matplotlib.org/) - Utilitzada per generar i mostrar els gràfics
* [NetworkX](https://networkx.github.io/documentation/stable/) - Utilitzada per generar els graf que representa una enquesta
* [Pickle](https://docs.python.org/3.6/library/pickle.html) - Utilitzada per guardar estructures de dades

## Authors

* **Albert Pita Argemi**

## Acknowledgments

* A tots aquells que m'han respost i ajudat a resoldre els dubtes que m'han anat sorgint durant la realització d'aquest projecte.
