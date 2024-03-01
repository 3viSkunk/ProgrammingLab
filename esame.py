class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name
        if not isinstance(self.name, str):
            raise ExamException("Nome del formato non corretto")       
    
    def get_data(self):
        time_series = []
        anno_prc = None
        mese_prc = None 
        try:
            with open(self.name, 'r' ) as file:
                for line in file:
                    riga = line.strip().split(',')
                    #controllo se la riga ha almeno due elementi
                    if len(riga)<2:
                        continue
                    #elimino l'intestazione
                    if riga[0] != "date":
                        anno_mese = riga[0].split('-')
                    else:
                        continue 
                    #nello split se non contiene almeno due elementi non è utile
                    if len(anno_mese) < 2:
                        continue
                    #provo a convertire in intero 
                    try:                          
                        anno = int(anno_mese[0])                       
                        mese = int(anno_mese[1])
                    except ValueError:
                        continue                        
                    #controllo validità delle date affinchè i dati siano "reali"    
                    if anno<1850 or anno > 2500 or mese <= 0 or mese >12:
                        continue 
                        
                    #controllo se la riga contiene l'intestazione
                    if riga[1] != "passengers":
                        #controllo che il dato dei passeggeri sia intero 
                        try:
                            passeggeri = int(riga[1])  
                        except ValueError:
                            continue
                    else:
                        continue 
                    #controllo se il valore sia negativo
                    if passeggeri < 0:
                        continue
    
                    #faccio un controllo date nel caso il timestamp non fosse ordinato 
                    if anno_prc is not None and (anno_prc > anno or anno_prc == anno):
                        if anno_prc > anno:
                          raise ExamException("Timestamp non ordinato")
                        if mese_prc is not None and mese_prc > mese:
                            raise ExamException("TimeStamp non ordinato")
                        if mese_prc is not None and (anno_prc == anno and mese_prc == mese):
                            raise ExamException("TimeStamp duplicato")
                        if mese_prc is None and (anno_prc == anno and mese == 12):
                            raise ExamException("TimeStamp duplicato")

                    if mese < 10:
                        mese_str = f"0{mese}"
                    else:
                        mese_str = str(mese)
                    #se supera i contolli posso appendere la lista
                    time_series.append([f"{anno}-{mese_str}", passeggeri])
                    #setto le variabili di appoggio per il prossimo controllo 
                    anno_prc = anno
                    mese_prc = mese 
                    if mese == 12:
                        mese = None 

            return time_series        
                    
        except FileNotFoundError:
            raise ExamException("File non trovato: specifica un file csv esistente")



def find_min_max(time_series):
    min_max = {}

    # creo il dizionario min_max con i dati relativi a ciascun anno
    # faccio i solito split 
    for dati in time_series:
        anno_mese = dati[0].split('-')
        anno = anno_mese[0]
        mese = anno_mese[1]
        passeggeri = dati[1]
        #prima cosa controllo se l'anno è già presente nel dizionario
        #se non esiste creo un dizionario di dizionari con valori di default
        if anno not in min_max:
            min_max[anno] = {"min_pss": 999999999, "max_pss": -999999999, "min": [], "max": []}

        #controllo i passeggeri se sono minori del valore associato a quello già presente lo cambio
        if passeggeri < min_max[anno]["min_pss"]:
            min_max[anno]["min_pss"] = passeggeri
            min_max[anno]["min"] = [mese]
        #conttrollo se sono uguali, nel caso appendo il mese alla lista corrispondente
        elif passeggeri == min_max[anno]["min_pss"]:
            min_max[anno]["min"].append(mese)
            
        #stesso procedimento nel caso siano maggiori numero di passeggeri
        if passeggeri > min_max[anno]["max_pss"]:
            min_max[anno]["max_pss"] = passeggeri
            min_max[anno]["max"] = [mese]
        elif passeggeri == min_max[anno]["max_pss"]:
            min_max[anno]["max"].append(mese)

    #rimuovo i valori dei passeggeri non richiesti dal dizionario
    for anno in min_max:
        del min_max[anno]["min_pss"]
        del min_max[anno]["max_pss"]

    return min_max
  