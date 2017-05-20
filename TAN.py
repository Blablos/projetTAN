#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wave; 
import math
import binascii

print ("ouverture du fichier")
NomFichier = 'testProjetTAN.wav'
Monson = wave.open(NomFichier,'w')

K = 4

nbCanal = 2    # stéreo
nbOctet = 1    # taille d'un échantillon : 1 octet = 8 bits
fe = 44100*K   # fréquence d'échantillonnage

frequenceG = float(input('Fréquence du son du canal de gauche (Hz) ? '))
frequenceD = float(input('Fréquence du son du canal de droite (Hz) ? '))
niveauG = float(input('Niveau du son du canal de gauche (0 à 1) ? '))
niveauD = float(input('Niveau du son du canal de droite (0 à 1) ? '))
duree = float(input('Durée (en secondes) ? '))

nbEchantillon = int(duree*fe)
print("Nombre d'échantillons :",nbEchantillon)

parametres = (nbCanal,nbOctet,fe,nbEchantillon,'NONE','not compressed')# tuple
Monson.setparams(parametres)    # création de l'en-tête (44 octets)

# niveau max dans l'onde positive : +1 -> 255 (0xFF)
# niveau max dans l'onde négative : -1 ->   0 (0x00)
# niveau sonore nul :                0 -> 127.5 (0x80 en valeur arrondi)

amplitudeG = 127.5*niveauG
amplitudeD = 127.5*niveauD

print('Veuillez patienter...')
for i in range(0,nbEchantillon):
    # canal gauche
    # 127.5 + 0.5 pour arrondir à l'entier le plus proche
    
    #porteuse =SIN(2*PI()*f0*'t')
    valG = wave.struct.pack('B',int(128.0 + amplitudeG*math.sin(2.0*math.pi*frequenceG*i/fe)))
    # canal droit
    valD = wave.struct.pack('B',int(128.0 + amplitudeD*math.sin(2.0*math.pi*frequenceD*i/fe)))
    Monson.writeframes(valG + valD) # écriture frame
    

Monson.close()

Fichier = open(NomFichier,'rb')
data = Fichier.read()
tailleFichier = len(data)
print('\nTaille du fichier',NomFichier, ':', tailleFichier,'octets')
print("Lecture du contenu de l'en-tête (44 octets) :")
print(binascii.hexlify(data[0:44]))
print("Nombre d'octets de données :",tailleFichier - 44)
Fichier.close()


#suechantilloner le signal en fe= k*fe

[Bloc de déclaration d'un fichier au format WAVE]
   FileTypeBlocID  (4 octets) : Constante «RIFF»  (0x52,0x49,0x46,0x46)
   FileSize        (4 octets) : Taille du fichier moins 8 octets
   FileFormatID    (4 octets) : Format = «WAVE»  (0x57,0x41,0x56,0x45)

[Bloc décrivant le format audio]
   FormatBlocID    (4 octets) : Identifiant «fmt »  (0x66,0x6D, 0x74,0x20)
   BlocSize        (4 octets) : Nombre d'octets du bloc - 16  (0x10)

   AudioFormat     (2 octets) : Format du stockage dans le fichier (1: PCM, ...)
   NbrCanaux       (2 octets) : Nombre de canaux (de 1 à 6, cf. ci-dessous)
   Frequence       (4 octets) : Fréquence d'échantillonnage (en hertz) [Valeurs standardisées : 11025, 22050, 44100 et éventuellement 48000 et 96000]
   BytePerSec      (4 octets) : Nombre d'octets à lire par seconde (c.-à-d., Frequence * BytePerBloc).
   BytePerBloc     (2 octets) : Nombre d'octets par bloc d'échantillonnage (c.-à-d., tous canaux confondus : NbrCanaux * BitsPerSample/8).
   BitsPerSample   (2 octets) : Nombre de bits utilisés pour le codage de chaque échantillon (8, 16, 24)

[Bloc des données]
   DataBlocID      (4 octets) : Constante «data»  (0x64,0x61,0x74,0x61)
   DataSize        (4 octets) : Nombre d'octets des données (c.-à-d. "Data[]", c.-à-d. taille_du_fichier - taille_de_l'entête  (qui fait 44 octets normalement).
   DATAS[] : [Octets du Sample 1 du Canal 1] [Octets du Sample 1 du Canal 2] [Octets du Sample 2 du Canal 1] [Octets du Sample 2 du Canal 2]

