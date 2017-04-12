import wave; """ wave = biblioteque de lecture/ecriture de .wav """
import math
import binascii


epsilon=[] """ erreur locale """
epsilonPrime=[] """ erreur restante sur l'echantillon n°n apres avoir choisi le code et compte tenu de l'erreur passe """
e=[] """ erreur passee reportee sur l'echantillon n°n """
y=[] """ valeur de sortie """
x=[] """ valeur d'entree """

""" j'ai verifie une bonne partie de ce code, ca a l'air de marcher"""
print("Création d'un fichier audio au format WAV (PCM 8 bits stéréo 44100 Hz)")
print("Son de forme sinusoïdale sur chaque canal\n")

NomFichier = 'testProjetTAN.wav'
Monson = wave.open(NomFichier,'w') # instanciation de l'objet Monson

nbCanal = 2    # stéreo
nbOctet = 1    # taille d'un échantillon : 1 octet = 8 bits
fech = 44100   # fréquence d'échantillonnage

frequenceG = float(input('Fréquence du son du canal de gauche (Hz) ? '))
frequenceD = float(input('Fréquence du son du canal de droite (Hz) ? '))
niveauG = float(input('Niveau du son du canal de gauche (0 à 1) ? '))
niveauD = float(input('Niveau du son du canal de droite (0 à 1) ? '))
duree = float(input('Durée (en secondes) ? '))

nbEchantillon = int(duree*fech)
print("Nombre d'échantillons :",nbEchantillon)

parametres = (nbCanal,nbOctet,fech,nbEchantillon,'NONE','not compressed')# tuple
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
    valG = wave.struct.pack('B',int(128.0 + amplitudeG*math.sin(2.0*math.pi*frequenceG*i/fech)))
    # canal droit
    valD = wave.struct.pack('B',int(128.0 + amplitudeD*math.sin(2.0*math.pi*frequenceD*i/fech)))
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
""" fin du code utilise """

""" TODO initialisation de x """



