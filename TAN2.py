"""declaration des variables"""

"""parametres modulables"""
f0=32000; """frequence porteuse"""
Q=4;"""coefficient d'echantillonnage"""
K=16;"""coefficient de suréchantillonnage du one bit DAC"""
r0=1;"""coefficient du report d erreur"""
V0=0;"""valeur tension pour coder 0""" 
V1=3;"""valeur de tension pour coder 1"""
alpha=0.93;"""pôle numérique du filtre reconstructeur"""

"""parametres calcules"""
fe=f0*Q;"""frequence d echantillonnage"""
fe2=f0*K;"""frequence de surechantillonnage"""
T0=1/f0;"""periode porteuse"""
Te2=1/fe2;"""periode de surechantillonnage"""
N=T0/Te2;"""nombre de surechantillons/periode porteuse"""
Vt=(V0+V1)/2;"""seuil pour coder 1 ou 2"""

"""-----------------------------------------------------"""

"""initialisation des variables a calculer"""

n=len(s);"""taille du fichier audio en bits"""
t=[];"""temps"""
x=[];"""porteuse normalise"""
c=[];"""code"""
e=[0];"""erreur reportee, au debut a 0"""
epsilon=[];"""erreur locale"""
epsilon2=[];"""erreur restante"""
yLisse=[0];"""y reconstruit"""

"""-------------------------------------------------------"""

"""calcul des variables a calculer"""

for i in range(0,n):
    """calcul de t"""
    t.append(i*Te2);
    """calcul de x"""
    x.append(s[i]*Vt+Vt);
    """calcul de c"""
    if(x[i]-e[i]-Vt>0):
        c.append(1);
    else:
        c.append(0);
    """calcul de y"""
    if (c[i]==0):
        y=V0;
    else:
        y=V1;
    """calcul de epsilon"""
    epsilon.append(y[i]-x[i]);
    """calcul de epsilon2"""
    epsilon2.append(epsilon[i]+e[i]);
    """calcul de e[i+1]"""
    e.append(r0*epsilon2[i]);
    """calcul de yLisse[i+1]"""
    if (i!=0):
        yLisse.append(y[i]*(1-alpha)+alpha*yLisse[i-1]);

