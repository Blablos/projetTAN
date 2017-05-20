#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wave
import binascii


print ("ouverture du fichier")
NomFichier = 'testProjetTAN.wav'
Monson = wave.open(NomFichier,'r')


print("\nNombre de canaux :",Monson.getnchannels())
print("Taille d'un échantillon (en octets):",Monson.getsampwidth())
print("Fréquence d'échantillonnage (en Hz):",Monson.getframerate())
print("Nombre d'échantillons :",Monson.getnframes())
print("Type de compression :",Monson.getcompname())

TailleData = Monson.getnchannels()*Monson.getsampwidth()*Monson.getnframes()

print("Taille du fichier (en octets) :",TailleData + 44)
print("Nombre d'octets de données :",TailleData)

print("\nAffichage d'une plage de données (dans l'intervalle 0 -",Monson.getnframes()-1,")")

echDebut = int(input('N° échantillon (début) : '))
echFin = int(input('N° échantillon (fin) : '))

print("\nN° échantillon	Contenu")

Monson.setpos(echDebut)
plage = echFin - echDebut + 1
x= []
for i in range(0,plage):
    print(Monson.tell(),'\t\t',binascii.hexlify(Monson.readframes(1)))
    x.append(binascii.hexlify(Monson.readframes(1)))
    print(x[i])

Monson.close()




epsilon1 = [] #erreur restante sur l'échantillon n°n après avoir choisi le code de sortie et compte tennu de l'erreur passée

epsilon = [] #erreur locale

e = [] #erreur passée reportée sur l'échantillon n°n

y = [] #valeur de sortie


b/ Quantification

Si on ne tient compte que de l'erreur locale :

epsilon[n] = y[n] - x[n]

dont on cherche à minimiser la valeur absolue, le code le plus exact à sortir est :

x[n] > Vt => c = 1
x[n] < Vt => c = 0

avec tension de seuil Vt = (V0+V1)/2
V0 = tension pour 1
v1 = tension pour 0

ce qui peut s'écrire :

c[n] = GAMMA( x[n] - Vt )

Ensuite :

y[n] = V0 si c[n] = 0
y[n] = V1 si c[n] = 1


c/ Prise en compte de l'erreur passée

Maintenant si on tient compte de l'erreur reportée e[n] depuis le passé,
on va chercher à la compenser en remplaçant x[n] par x[n] - e[n]

Par exemple, l'échantillon précédent était trop grand à cause de l'erreur restante,
et on va essayer d'abaisser le présent d'une partie e[n] de cette erreur pour compenser.

D'où :

c[n] = GAMMA( x[n] - e[n] - Vt )


d/ Calcul du report d'erreur passée

Maintenant, on peut envisager de ne reporter sur l'échantillon n° n
qu'une part ro de l'erreur restante au dernier échantillon n° n-1 :

e[n] = ro * epsilon'[n-1]

avec le coefficient ro dans l'intervalle [0 ; 1 ]

Enfin, après avoir choisi le code c[n], on aura une erreur locale :

epsilon[n] = y[n] - x[n]

à laquelle s'ajoute l'erreur reportée pour avoir l'erreur restante n° n :

epsilon'[n] = epsilon[n] + e[n]


e/ Résumé de l'algorithme intuitif

e[n] = ro * epsilon'[n-1]

c[n] = GAMMA( x[n] - e[n] - Vt )

y[n] = V0 si c[n] = 0

y[n] = V1 si c[n] = 1

epsilon[n] = y[n] - x[n]

epsilon'[n] = epsilon[n] + e[n]



2. RELATION AVEC LA FICHE

a/ Introduction

Maintenant voyons comment cet algorithme "intuitif" peut s'interpréter.

Dans l'erreur  y[n] - x[n]
seule la partie qui tombe dans la bande spectrale audible est gênante.

Cette dernière peut être obtenue en appliquant un filtre passe-bas H sur l'erreur:

H{ y[n] - x[n] }

Par conséquent, cet algorithme "intuitif" est simplement un cas particulier
avec le filtre de transformée en z :

H(z) = 1 / (1 - ro x z^-1)

qui est un simple passe-bas du premier ordre avec un pôle :

z1 = ro

(on a bien ro < 1, sinon le la boucle de calcul est instable et l'agorithme diverge).


b/ Etude du filtre

On note que si on représente H par une fraction rationnelle en z
dont le numérateur est un polynôme en z^-n avec des coefficients b[n]
et le dénominateur avec a[n]

On a alors ici les coefficients suivants :

b[0] = 1
b[m] = 0 sinon

a[0] = 1
a[1] = -ro
a[m] = 0 sinon

c/ Cas particulier où ro = 1

Le cas particulier où ro = 1 est intéressant:

on a le pôle en s1 = fe' * Ln(ro) = 0, H est alors un simple intégrateur.

L'algorithme devient alors le "Sigma-Delta Modulator" (SDM) de la littérature.



3. ESSAI

J'ai essayé de faire rapidement un essai sur Excel afin de bien voir les relations entre les nombres,
et ça marche (fichier joint).

On obtient bien la sinusoïde de départ.

Il semble finalement qu'un filtre d'ordre 1 avec un pôle en z1 = 1 est suffisant.
Ce fichier de test Excel permet de voir un "one bit DAC" au 1er ordre à l'oeuvre.

Il affiche le signal reconstruit.

On peut faire varier les divers paramètres, le réglage semble le meilleur,
et changer V1 et V0 (ici appelés Vmax et Vmin) ne change rien
(à condition de faire attention à ce que le signal à convertir soit dans [Vmin ; Vmax]
ce qui est assuré ici dans "porteuse_normalisée"

Le pôle du filtre reconstructeur est placé à peu près sur f0.

(L'algorithme utilisé, sa justification et relation avec le calcul fourni sont décrits
dans une fiche à part).

Le filtre H de pondération d'erreur est du premier ordre:

a0 = 1
a1 = - ro
b0 = 1

ro dans [0 ; 1 ] = pôle qui devrait couper à fe/2 environ;
mais marche bien quand on le met à 1 (coupure à 0Hz: intégrateur pur).


Le signal n'est pas parfait, mais :


1/ le filtre passe-bas de reconstruction n'est aussi qu'à l'ordre 1 !

En réalité, on utilise un ordre 2 (une self et un condensateur) pour ce genre de filtre,
(sans compter le transducteur qui lisse encore)
et donc les petits parasites (qui sont essentiellement de fréquence > fe/2) devraient être fortement atténués.


2/ la fréquence d'échantillonnage de base n'est que de 4 fois cette fréquence ;
imaginons un signal échantillonné en PCM reconstruit avec un filtre d'ordre 1:
ce serait nettement pire.


3/ avec un filtre de DAC d'ordre supérieur à 1 on devrait améliorer;


4/ on note que les petits parasites forment un signal assez régulier avec des périodes,
et donc forment des pics dans le spectre.

Le fait d'ajouter du "dithering" devrait nettement améliorer ce point.


5/ avec du "dithering" et un filtre d'ordre 2 en sortie c'est déjà pas trop mal.

