#! -*- coding: utf-8 -*-
import re

class EnterpriseFormFilter(object):
    '''
    Cleaning criterion that standarizes legal forms of
    enterprises
    '''
    
    def __init__(self):
        self.base_repl = (
        (re.compile(r"\bSOCIET.",flags=re.I), ' SOCIETA '),    
        (re.compile(r"\bSOCI\sET.'?",flags=re.I), 'SOCIETA'),
        (re.compile(r"\bSOCIET.'?\s*(CONSORTILE\s*)?PER\s+AZIONI",flags=re.I), 'SPA'),    
        (re.compile(r"\bSOCIET.'?\s+A\s+RESP(ONSABILIT.'?)\s+LIMITATA",flags=re.I), 'SRL'),
        (re.compile(r"\bS[. ]*?C[. ]*?A[. ]*?R[. ]*?L[.]*?\b",flags=re.I),'SCARL'),
        (re.compile(r"\bC[. ]*?O[. ]*?O[. ]*?P[.]*?\b",flags=re.I),'COOP'),
        (re.compile(r"\bG[. ]*?M[. ]*?B[. ]*?H[.]*?\b",flags=re.I),'GMBH'),
        (re.compile(r"\bI[. ]*?R[. ]*?B[. ]*?M[.]*?\b",flags=re.I),'IRBM'),
        (re.compile(r"\bS[. ]*?A[. ]*?P[. ]*?A[.]*?\b",flags=re.I),'SAPA'),
        (re.compile(r"\bS[. ]*?A[. ]*?R[. ]*?L[.]*?\b",flags=re.I),'SARL'),
        (re.compile(r"\bS[. ]*?C[. ]*?R[. ]*?L[.]*?\b",flags=re.I),'SCRL'),
        (re.compile(r"\bS[. ]*?C[. ]*?P[. ]*?A[.]*?\b",flags=re.I),'SCPA'),
        (re.compile(r"\bI[. ]*?N[. ]*?C[.]*?\b",flags=re.I),'INC'),
        (re.compile(r"\bL[. ]*?L[. ]*?C[.]*?\b",flags=re.I),'LLC'),
        (re.compile(r"\bL[. ]*?T[. ]*?D[.]*?\b",flags=re.I),'LTD'),
        (re.compile(r"\bN[. ]*?M[. ]*?N[.]*?\b",flags=re.I),'NMN'),
        (re.compile(r"\bP[. ]*?L[. ]*?C[.]*?\b",flags=re.I),'PLC'),
        (re.compile(r"\bS[. ]*?A[. ]*?S[.]*?\b",flags=re.I),'SAS'),
        (re.compile(r"\bS[. ]*?C[. ]*?H[.]*?\b",flags=re.I),'SCH'),
        (re.compile(r"\bS[. ]*?N[. ]*?C[.]*?\b",flags=re.I),'SNC'),
        (re.compile(r"\bS[. ]*?P[. ]*?A[.]*?\b",flags=re.I),'SPA'),
        (re.compile(r"\bS[. ]*?R[. ]*?L[.]*?\b",flags=re.I),'SRL'),
        (re.compile(r"\bS[. ]*?R[. ]*?1[.]*?\b",flags=re.I),'SRL'),
        (re.compile(r"\bA[. ]*?G[.]*?\b",flags=re.I),'AG'),
        (re.compile(r"\bC[. ]*?O[.]*?\b",flags=re.I),'CO'),
        # ABBREVIAZIONI
        (re.compile(r"\b(CON\s+)?DENOMINAZIO?NE ABBREVIATA\b.*$",flags=re.I), ''),
        (re.compile(r"\bOPPURE\b.*$",flags=re.I), ''),
        (re.compile(r"\bIN ABBREVIAZIONE\b.*$",flags=re.I), ''),
        (re.compile(r"\bO PER BREVIT.'?\b.*$",flags=re.I), ''),
        (re.compile(r"\bIN ACRONIMO\b.*$",flags=re.I), ''),
        (re.compile(r"\bDA USARSI\b.*$",flags=re.I), ''),
        (re.compile(r"\b(O\s+)?IN FORMA ABBREV(IATA)?\b.*$",flags=re.I), ''),
        (re.compile(r"\b(O\s+)?PER\s+ESTESO\b.*$",flags=re.I), ''),
        (re.compile(r"\bABBREVIABILE\b.*$",flags=re.I), ''),
        (re.compile(r"\b(E\s)?PIU BREVEMENTE\b.*$",flags=re.I), ''),
        (re.compile(r"\b(DETTA|ENUNCIABILE) ANCHE\b.*$",flags=re.I), ''),
        (re.compile(r"IN BREVE\b.*$",flags=re.I), ''),
        (re.compile(r"\bIN SIGLA\b.*$",flags=re.I), ''),
        (re.compile(r"\bSIGLABILE\b.*$",flags=re.I), ''),
        (re.compile(r"\bIN ABBREVIATED FORM\b.*$",flags=re.I), ''),
        # LIQUIDAZIONE E FALLIMENTO
        (re.compile(r"(SOCIETA\s+)?IN\s+LIQU(IDAZIONE?)?.*$",flags=re.I), ''),
        (re.compile(r"IN\s+FALLIMENTO\b.*$",flags=re.I), ''),
        
        (re.compile(r"\bIN\+sBREVE\b.*$"),''),
        (re.compile(r'\bIN\+sSIGL\b.*$'),''),
        (re.compile(r'\bIN\+sFORMA\+sABBREVIATA\b.*$'),''),
        (re.compile(r'\bBREVEMENTE\+sANCHE\b.*$'),''),
        (re.compile(r'\bANCHE\+sIN\+sFORMA\+sAB\b.*$'),''),
         
        # SOCIETA RICONOSCIUTE
        (re.compile(r"\bA[. ]*?R[. ]*?L[. ]*?\b",flags=re.I),'ARL'),
        (re.compile(r"((ONLUS)\s+)?\bORGANIZZAZIONE NON LUCRATIVA DI UTILITA SOCIALE\b",flags=re.I), 'ONLUS'),
        (re.compile(r"([^\s])SOCIET.'?",flags=re.I), r'\1 SOCIETA'),
        (re.compile(r"\bRE\s?SP(ON(SABILIT.'?)?)?\b"),'RESPONSABILITA'),
        (re.compile(r"\bSOC\b",flags=re.I), 'SOCIETA'),
        (re.compile(r"\bSOCIET.\'?(\s|\Z)",flags=re.I), ' SOCIETA '),
        (re.compile(r"\bCOOP\b",flags=re.I), 'COOPERATIVA'),
        (re.compile(r"\bA\s+(RL|RESPONSABILITA(\s+LIMI(T(ATA)?)?)?)\b",flags=re.I), 'ARL'),
        (re.compile(r"\b(?:SOCIETA)?\s+COOPERATIVA\s+(DI PRODUZIONE E LAVORO|AGRICOLA|SOCIALE|EDILIZIA)(\s+\bPER\s+AZIONI\b)",flags=re.I), r' SCPA \1'),
        (re.compile(r"\b(?:SOCIETA)?\s+COOPERATIVA\s+(DI PRODUZIONE E LAVORO|AGRICOLA|SOCIALE|EDILIZIA)(\s+\bARL\b)(\s+ONLUS)?",flags=re.I), r' SCRL \1'),
        (re.compile(r"\bSOCIETA\s*COOPERATIVA(\s+\bARL\b)?(\s+ONLUS)?",flags=re.I), ' SCRL '),
        (re.compile(r"\bSOCIETA\s+CONSORTILE\s+P(ER)?\s+A(ZIONI)?\b",flags=re.I), ' SCPA '),        
        (re.compile(r"\bSOCIETA\s+CONSORTILE\s+ARL\b",flags=re.I), ' SCARL '),
        (re.compile(r"\bSOCIETA\s+PER\s+AZIONI\b",flags=re.I), ' SPA '),        
        (re.compile(r"\b(?:SOCIETA)\s+(AGRICOLA|SOCIALE|EDILIZIA)(\s+\bARL\b)?(\s+ONLUS)?",flags=re.I), r' SRL \1'),
        (re.compile(r"\bSOCIETA\s+ARL\b",flags=re.I), ' SRL '),
        (re.compile(r"\bSOCIETA\s+IN\s+ACCOMANDITA\s+PER\sAZIONI?",flags=re.I), ' SAA '),
        (re.compile(r"\bSCRL\s+CONSORTILE\b",flags=re.I), ' SXRL '),
        (re.compile(r"\bSOCIETA\s+IN\s+NOME\s+COLLETTIVO\b",flags=re.I),' SNC '),
        # UNIPERSONALI
        (re.compile(r"\bSRL\s+(SOCIETA\s+)?(UNI(PERSONALE|NOMINALE)|CON\s+SOCIO\s+UNICO)\b",flags=re.I), ' SRLU '),
        (re.compile(r"\bSPA\s+(SOCIETA\s+)?(UNI(PERSONALE|NOMINALE)|CON\s+SOCIO\s+UNICO)\b",flags=re.I), ' SPAU '),
        (re.compile(r"\bSRL\s+([A-Z]+)\s+(SOCIETA\s+)?(UNI(PERSONALE|NOMINALE)|CON\s+SOCIO\s+UNICO)\b",flags=re.I), r' \1 SRLU '),
        #(re.compile(r"\bPATENT\s+DEP(ARTMEN)?T\b"), ''),
        #(re.compile(r"\bPATDPT\b"), ''),
        #(re.compile(r"\bPATENT\s+DPMT\b"), ''),
        (re.compile(r"\s*\bPAT(ENT)?\s+(DEP|DE?PT?(AR)?M?T(MENT)?)\b\s*",flags=re.I), ' '),  
        
        
        # PULIZIE GENERALI
        (re.compile(r"\b\d+$",flags=re.I), ''), # numbers at the end of the string
        
        (re.compile(r"\b.$",flags=re.I), ''),
        #(re.compile(r"[.\s,]+",flags=re.I), ''),
        (re.compile(r"[.,]+",flags=re.I), ''),  
        (re.compile(r"^\s+",flags=re.I), ''),
        (re.compile(r"\s+$",flags=re.I), ''),
        (re.compile(r"[^\&\/A-ZÀÈÉÌÒÙ0-9]",flags=re.I), ' '), 
        (re.compile(r"[^\&\/A-ZÀÈÉÌÒÙ0-9]",flags=re.I), ' '),
        (re.compile(r"^\s+",flags=re.I), ''),
        (re.compile(r"\s+$",flags=re.I), ''),
        # deletes digits only
        (re.compile(r"^[\d\/]+$",flags=re.I), ''),    
        (re.compile(r"\b\s-\s\b",flags=re.I), ''),# elimina ' - '
        
        (re.compile(r"\b.$",flags=re.I), ''),
        (re.compile(r"\s+$",flags=re.I), '')
        )
    
    
    def cleanValue(self, v):
        v2=v
        if v2 is not None:
            for ptrn, repl in self.base_repl:
                v2=re.sub(ptrn, repl, v2)
        return v2
    