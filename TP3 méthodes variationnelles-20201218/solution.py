#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 14:48:27 2019

@author: said
"""
#%% Solutiuons

#%% 1.1 question théorique
#
#%% Q1.2
# lire l'image au format float directement
myim=np.float32(skio.imread('lena.tif'))
# voir l'image
viewimage(myim,titre='ORIGINALE')
#degrader une image

imb=degrade_image(myim,25)

# voir l'image bruitée
viewimage(imb,titre='BRUITEE')

# COMMENTAIRE: restauration quadratique : on fait varier lamb
# on remarque que pour lamb tres petit le programme ne fait rien.
# pour lamb tres grand l'image devient flou
lamb=0.0001
restau=minimisation_quadratique(imb,lamb)
viewimage(restau,titre='RESTQUAD_LAMB='+str(lamb))

lamb=0.1
restau=minimisation_quadratique(imb,lamb)
viewimage(restau,titre='RESTQUAD_LAMB='+str(lamb))

lamb=1
restau=minimisation_quadratique(imb,lamb)
viewimage(restau,titre='RESTQUAD_LAMB='+str(lamb))

lamb=100
restau=minimisation_quadratique(imb,lamb)
viewimage(restau,titre='RESTQUAD_LAMB='+str(lamb))

#%% 1.3
imb=degrade_image(myim,5)

but=norm2(imb-myim)
lmin=0.001
lmax=1
resmin=minimisation_quadratique(imb,lmin)
resmax=minimisation_quadratique(imb,lmax)
errmin=norm2(imb-resmin)
errmax=norm2(imb-resmax)
for k in range(10): # on fait dix dichotomies
    lmil=(lmin+lmax)/2
    resmil=minimisation_quadratique(imb,lmil)
    errmil=norm2(resmil-imb)
    if errmil>but:
        lmax=lmil
        errmax=errmil
        resmax=resmil
    else:
        lmin=lmil
        errmin=errmil
        resmin=resmil
# ON trouve le lambda qui respecte la norme de l'attache aux donnees theorique
        # egal a lmil=0.331
#%% 1.4
vk=np.arange(-1,0,0.05) # on tatonne pour trouver ces valeurs -1 et 0
errbest=norm2(imb)+10
for k in vk:
    lamb=10**k
    res=minimisation_quadratique(imb,lamb)
    err=norm2(myim-res)
    print(lamb,err)
    if err<errbest:
        lambest=lamb
        errbest=err

print(lambest) # on trouve le meilleur lambda pour lambda=0.11 En tout cas moins que lambda de l'attache aux données

#%% 2.1
imb=degrade_image(myim,25)
(u,energ)=minimise_TV_gradient(imb,1,0.1,100)   # pas = 0.1
(u,energ2)=minimise_TV_gradient(imb,1,1,100)       # pas = 1
plt.plot(energ) 
plt.plot(energ2)
# Commentaires : On constate qu'une descente de gradient a pas constant
# fonctionne tres mal avec la variation totale. 
# Parfois l'énergie augmente même apres avoir baissé
#%% 2.2
# La methode chambolle minimise et minimise_TV_gradient minimisent une energie qui
# correspond au gradient non périodique
# ATTENTION IL Y AVAIT UN BUG DANS LE CALCUL DE gradient_TV (la nouvelle version est sur le site)

# D'abord on calcule un bon minimiseur avec gradient TV (calcul tres lent)
(u001,energ001)=minimise_TV_gradient(imb,40,0.1,100)

E2grad=E2_nonperiodique(u001,imb,40)

uchamb=vartotale_Chambolle(imb,40,itmax=30)
E2chamb=E2_nonperiodique(uchamb,imb,40)
print(E2chamb/E2grad)
# Pour obtenir des energies equivalentes il faudrait faire 1000 pas de descente
# de gradient avec un pas de 0.01
#%% partie 3
imb=degrade_image(myim,25)

# d'abord le lambda optimal pour la partie quadratique.
vk=np.arange(-1,1,0.05) # on tatonne pour trouver ces valeurs -1 et 0
errbest=norm2(imb)+10
for k in vk:
    lamb=10**k
    res=minimisation_quadratique(imb,lamb)
    err=norm2(myim-res)
    print(lamb,err)
    if err<errbest:
        lambest=lamb
        errbest=err

print(lambest) 
lambestquad=lambest # = 1.1220184543019658
restquad=minimisation_quadratique(imb,lambestquad)
errquad=norm2(restquad-myim)
viewimage(restquad,titre='BESTQUAD')
#%% La partie variation totale
vk=np.arange(1.39,1.8,0.02) # on tatonne pour trouver ces valeurs 1.39 et 1.8
errbest=norm2(imb)+10
for k in vk:
    lamb=10**k
    res=vartotale_Chambolle(imb,lamb)
    err=norm2(myim-res)
    print(lamb,err)
    if err<errbest:
        lambest=lamb
        errbest=err

print(lambest) 
lambestvartotale=lambest # =40.73802778041128
restvartotale=vartotale_Chambolle(imb,lambestvartotale)
errvar=norm2(restvartotale-myim)
viewimage(restvartotale,titre='BESTVARTOTALE')
#%%

# COMMENTAIRE: D'une part errvar est plus petite que errquad
# L'image resultante est aussi qualitativement bien meilleure. Les bords 
# sont mieux respectés dans l'image restvartotale
 