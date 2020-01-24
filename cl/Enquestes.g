grammar Enquestes;

root : enquestes+ EOF;

enquestes : pregunta
        | resposta
        | item 
        | enquesta
        | alternativa
        | 'END'
        ;

pregunta : ID ':' 'PREGUNTA' TextP;

resposta : ID  ':' 'RESPOSTA' opcions+;

opcions : NUM ':' TextR;

item : ID ':' 'ITEM' assignacio;

assignacio : ID '->' ID;

enquesta : ID ':' 'ENQUESTA' ID+;

alternativa : ID ':' 'ALTERNATIVA' ID '[' opt_alternativa ']';

opt_alternativa : '(' NUM ',' ID ')' (',' '(' NUM ',' ID ')')*;

ID : [a-zA-Z][a-zA-Z0-9]*;
TextP : [ a-zA-Z\u0080-\u00FF]+[?];
TextR : [ a-zA-Z\u0080-\u00FF]+[;];
NUM : [0-9]+;
WS : [\r]*[ \n]+ -> skip;
