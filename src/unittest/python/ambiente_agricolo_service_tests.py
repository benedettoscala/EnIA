import unittest
import os, sys

from mockito import mock, when
sys.path.append(os.path.abspath(os.path.join('.' )))
from src.logic.Storage.TerrenoDAO import TerrenoDAO
from src.logic.AmbienteAgricolo.AmbienteAgricoloService import AmbienteAgricoloService
from src.dbConnection import terreni
from src.logic.model.Terreno import Terreno

"""
    IMPORTANTISSIMO: QUESTE SONO SOLO TEST DI ESEMPIO, QUANDO INZIEREMO A FARLI DOBBIAMO TASSATIVAMENTE
    SEGUIRE IL TCS
"""
class AmbienteAgricoloServiceTest(unittest.TestCase):
    
    # Arrange
    
    
    def test_visualizzaTerreni(self):
        # Arrange
        print("visualizzaTerreni")
        farmer = "63b9e6a27862c31f1f7b221f"
        # Act
        
        terreni = AmbienteAgricoloService.visualizzaTerreni(farmer)

        # Assert
    
        self.assertEqual(terreni[0].id, "63c6ca0e895a27206d95c005")
        self.assertEqual(terreni[0].proprietario, "63b9e6a27862c31f1f7b221f")
    
    #Limoni non sono una coltura valida
    #Controllo colture non dovrebbe essere il formato ma se esistono tra quelle preinserite
    
    def test_eliminaTerreno(self):
        print("Elimina Terreno")
        #Creo il Terreno
        nome = "Terreno-B"
        coltura = "Orzo"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato["restituito"])
        #Elimino il Terreno
        risultato2 = AmbienteAgricoloService.eliminaTerreno(risultato["restituito"]) 
        self.assertTrue(risultato2) #Eliminazione Riuscita
       
    #ORACOLO: Inserimento fallisce per formato del nome errato       
    def test_aggiungiTerreno_TC_2_1_1(self):
        print("TC_2_1_1")
        nome = "Ç?(&%U"
        coltura = "Orzo" 
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["nomeNonValido"], True) #Fallito a causa del formato del nome
   
    #ORACOLO: Inserimento fallisce per nome mancante
    def test_aggiungiTerreno_TC_2_1_2(self):
        print("TC_2_1_2")
        nome = ""
        coltura = "Orzo"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["nomeNonValido"], True) #Fallito a causa della mancanza del nome     
    
    #ORACOLO: Inserimento fallisce per mancanza di coltura
    def test_aggiungiTerreno_TC_2_1_3(self):
        print("TC_2_1_3")
        nome = "Terreno-A"
        coltura = ""
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["colturaNonValida"], True) #Fallito a causa della mancanza della coltura
    
    #ORACOLO: Inserimento fallisce per formato invalido di coltura
    def test_aggiungiTerreno_TC_2_1_4(self):
        print("TC_2_1_4")
        nome = "Terreno-A"
        coltura = "*çéçé=("
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["colturaNonValida"], True) #Fallito a causa del formato sbagliato della coltura 
    
    #ORACOLO: Inserimento fallisce per formato invalido di coltura 
    #Si potrebbe eliminare in quanto una ripetizione del 4, stessi controlli.
    def test_aggiungiTerreno_TC_2_1_5(self):
        print("TC_2_1_5")
        nome = "Terreno-A"
        coltura = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap intoele"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["colturaNonValida"], True) #Fallito a causa del formato sbagliato della coltura                                   
        
    #2_1_6, 2_1_7 non si possono fare perchè la dimensione del terreno non esiste più.
    
    #ORACOLO: Fallisce in quanto manca la posizione
    def test_aggiungiTerreno_TC_2_1_8(self):
        print("TC_2_1_8")
        nome = "Terreno-A"
        coltura = "Limoni"
        posizione = {}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["posizioneNonValida"], True) #Fallito a causa dell'assenza della posizione
   
    #ORACOLO: Fallito per il formato sbagliato della posizione
    def test_aggiungiTerreno_TC_2_1_9(self):
        print("TC_2_1_9")
        nome = "Terreno-A"
        coltura = "Limoni"
        posizione = {"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"coordinates": [[12.682885346272485,42.42118547557695],[12.683224252299652,42.421660820429594]],"type": "LineString"}}]}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertEqual(risultato["esitoOperazione"], False)  #Fallito inserimento
        self.assertEqual(risultato["posizioneNonValida"], True) #Fallito a causa del formato sbagliato della posizione
    
    #2_1_10 è per preferito e non per priorità, va cambiato nel TCS.
    
    #ORACOLO: Fallito a causa del tipo sbagliato di preferito, che dovrebbe essere un bool e non un int.
    def test_aggiungiTerreno_TC_2_1_10(self):
        print("TC_2_1_10")
        nome = "Terreno-A"
        coltura = "Limoni"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = 45
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        self.assertRaises(TypeError)
    
    #Necessario cambiare coltura da Limoni ad Orzo nel Test Case
    #ORACOLO: Inserimento va a buon fine in quanto tutti i campi sono corretti.
    def test_aggiungiTerreno_TC_2_1_11(self):
        print("TC_2_1_11")
        nome = "Terreno-A"
        coltura = "Orzo"
        posizione = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[14.783607,40.772225],[14.783735,40.772745],[14.784594,40.771965],[14.783607,40.772225]]]}}
        preferito = True
        priorita = 15
        proprietario = "63b9e6a27862c31f1f7b221f"
        stadio_crescita = "Sviluppo"
        risultato = AmbienteAgricoloService.aggiungiTerreno(nome, coltura, stadio_crescita, posizione, preferito, priorita, proprietario)
        print(risultato)
        AmbienteAgricoloService.eliminaTerreno(risultato["restituito"])        
        self.assertEqual(risultato["esitoOperazione"], True)  #Inserimento riesce
        