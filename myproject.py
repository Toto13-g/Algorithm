# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:41:08 2024

@author: gargani
"""
import streamlit as st
import re

def Algorithm1(s_green,s_red):
   def Somme(liste):
       Somme = 0
       for i in liste:
           Somme = Somme + i
       return Somme

   def SoustractionListe(L1,L2):
       Liste = []
       for i in range(len(L1)):
           Liste.append(L1[i] - L2[i])
       return Liste

   def AdditionListe(L1,L2):
       Liste = []
       for i in range(len(L1)):
           Liste.append(L1[i]+L2[i])
       return Liste

   def Sign(L1):
       Liste = [-L1[k] for k in range(len(L1))]
       return Liste

   ### We compare societies of same population size.
   def TestPopulation(s_green,s_red):
       if Somme(s_green) != Somme(s_red):
           return False
       else:
           return True

   ### Two societies must also have the same number of categories.
   def TestCategory(s_green,s_red):
       if len(s_green) != len(s_red):
           return False
       else:
           return True
       
   ### We compute the values of the H curve
   def H(s):
       H = [0]
       for i in range(len(s)):
           if i == 0:
               H[i] = s[0]
           else:
               H.append(2*H[i-1] + s[i]) 
       return H

   ### We compute the values of the BarH curve
   def BarH(s):
       s.reverse()
       BarH = [0]
       for i in range(len(s)):
           if i == 0:
               BarH[i] = 0
           else:
               BarH.append(2*BarH[i-1] + s[i-1])
       s.reverse()
       return BarH

   ### We test if the H-dominance is verified.
   def TestHDominance(s_green,s_red):
       Test = []
       for i in range(len(s_green)):
           if H(s_green)[i] <= H(s_red)[i]:
               Test.append(1)
           else:
               Test.append(0)
       if Somme(Test) == len(s_green):
           return True
       else:
           return False

   ### We test if the BarH-dominance is verified.
   def TestBarHDominance(s_green,s_red):
       i = 0
       BHgreen = BarH(s_green)
       BHred = BarH(s_red)
       while i < len(s_green) and BHgreen[i] <= BHred[i]:
               i = i+1
       ### When the for is ended we check for dominance.
       if i == len(s_green):
           return True
       else:
           return False

   def TestDominance(s_green,s_red):
       if (TestBarHDominance(s_green,s_red) == True) and TestHDominance(s_green,s_red)== True:
           return True
       else:
           return False
   ### When a society s doesn't preserve the BarHdominance, we define
   ### the category hmax
   def hmax(s_green,s):
       i = len(s_green) - 1 
       BHgreen = BarH(s_green)
       BHs = BarH(s)
       BHgreen.reverse()
       BHs.reverse()
       while i >= 0 and BHgreen[i] <= BHs[i]:
               i = i - 1
       return i

   def hmin(s_green,s):
       i = 0
       Hgreen = H(s_green)
       Hs = H(s)
       while i <= len(s_green)-1 and Hgreen[i] <= Hs[i]:
           i = i + 1
       return i
       
   ### To define the preliminaries transfers we define the cumulative
   def DeltaCumulative(s_green,s_red):
       Delta_i = 0
       Delta = []
       for i in range(len(s_green)):
           Delta_i = Delta_i + s_red[i] - s_green[i] 
           Delta.append(Delta_i)
       return Delta

   DeltaCumulative([2,2,2], [3,0,3])

   ### We define the categories used for preliminaries transfer.
   def a_k(s_green,s_red):
       a_k =[]
       k = 0
       Delta = DeltaCumulative(s_green,s_red)
       while Delta[k] <= 0:
           k = k+1
       a_k.append(k)
       for i in range(k+1,len(Delta)):
           if Delta[i-1]<0 and Delta[i] >=0:
               a_k.append(i)
       return a_k
         
   ### We define a Hammond Transfer.
   def HammondTransfer(s,g,i,j,l):
       s_1 = [s[k] for k in range(len(s))]
       if i < j:
           s_1[g] = s[g] - 1
           s_1[i] = s[i] + 1
           s_1[j] = s[j] + 1
           s_1[l] = s[l] - 1
       else:
           s_1[g] = s[g] - 1
           s_1[i] = s[i] + 2
           s_1[l] = s[l] - 1
       return s_1

   def FirstConditions(s_green,s_red):
       if (TestCategory(s_green,s_red) == True) and (TestPopulation(s_green, s_red) == True) and (TestDominance(s_green, s_red) == True):
           return True
       else:
           if (TestCategory(s_green,s_red) == False):
               return 1
           elif (TestPopulation(s_green,s_red) == False):
               return 2
           elif (TestDominance(s_green, s_red) == False):
               if TestDominance(s_red, s_green) == False:
                   return 3
               else:
                   return 4
 
   if FirstConditions(s_green, s_red) == True:
        L = []
        while s_green != s_red and (TestDominance(s_green, s_red) == True):
             k = 0
             a = a_k(s_green, s_red)
             s_k = HammondTransfer(s_red, a[0], a[0] + 1, a[1]-1, a[1])
             while k < len(a)-2 and (TestBarHDominance(s_green, s_k) == True):
                    k = k + 1
                    s_k = HammondTransfer(s_red, a[k], a[k] + 1, a[k+1]-1, a[k+1])    
             if k == len(a) - 2 and (TestDominance(s_green, s_k) == True): ### Here the pair (aN-1, aN) preserves the double dominance.
                 S = SoustractionListe(s_k, s_red)
                 L.append(S)
                 s_red = s_k
             elif k == len(a) - 2 and (TestHDominance(s_green, s_k) != True): ### Here the pair (a_N-1, a_N) only preserves the BarH dominance.
                          if hmin(s_green,s_k) == a[len(a) - 1]: ### Proposition 4
                              Hammond = HammondTransfer(s_red, a[len(a)-2],a[len(a)-2] + 1, a[len(a)-2] + 1, a[len(a)-1])
                              S = SoustractionListe(Hammond, s_red)
                              L.append(S)
                              s_red = Hammond
                          if hmin(s_green,s_k) != a[len(a) - 1]: ###Propositions 5 and 6
                              rangehmin = []
                              Survival = Sign(DeltaCumulative(s_green, s_red))
                              for i in range(hmin(s_green, s_k),a[len(a)-1]+1):
                                  rangehmin.append(Survival[i])
                              if Somme(rangehmin) == len(rangehmin): ###Proposition 6
                                  Hammond = HammondTransfer(s_red, a[len(a)-2], a[len(a)-2]+1, hmin(s_green,s_k),a[len(a)-1])
                                  S = SoustractionListe(Hammond, s_red)                
                                  L.append(S)
                                  s_red = Hammond
                              else: #Proposition 5
                                   h = len(rangehmin) - 1
                                   while h >= 0 and rangehmin[h] < 2:
                                       h = h-1
                                   e = h + hmin(s_green, s_k)
                                   Hammond = HammondTransfer(s_red, a[len(a)-2], a[len(a)-2]+1,  a[len(a)-2]+1,e+1)
                                   S = SoustractionListe(Hammond, s_red)
                                   L.append(S)
                                   s_red = Hammond
             else: ### Here there is a pair that does not preserve the BarHdominance.
                       if k >= 1 and (TestHDominance(s_green,HammondTransfer(s_red, a[k-1], a[k-1] + 1, a[k]-1, a[k])) == True):
                           Hammond = HammondTransfer(s_red, a[k-1], a[k-1] + 1, a[k]-1, a[k])
                           S = SoustractionListe(Hammond, s_red)
                           L.append(S)
                           s_red = Hammond
                       else:
                           s_k = HammondTransfer(s_red, a[k], a[k] + 1, a[k+1]-1, a[k+1])
                           if hmax(s_green, s_k) <= a[k]: ## Proposition 1
                              Hammond = HammondTransfer(s_red, a[k], a[k+1]-1, a[k+1]-1, a[k+1]) 
                              S = SoustractionListe(Hammond, s_red)
                              L.append(S)
                              s_red = Hammond
                           else:
                               rangehmax = []
                               condition = []
                               Delta = DeltaCumulative(s_green, s_red)
                               for i in range(a[k],hmax(s_green, s_red)+1):
                                   rangehmax.append(Delta[i])
                               for D in rangehmax:
                                   if D <= 1:
                                       condition.append(0)
                                   else:
                                       condition.append(1)
                               if Somme(D) == 0: ### Proposition 3
                                   j = a[k] + 1
                                   while Delta[j] >= Delta[j-1] and j <= hmax(s_green, s_k)+1:
                                       j=j+1
                                   o = j + 1
                                   while Delta[o] <= Delta[o+1] and o <= a[k]+1:
                                       o = o + 1
                                   Hammond = HammondTransfer(s_red, a[k], j, o-1, o)    
                                   S = SoustractionListe(Hammond, s_red)
                                   L.append(S)
                                   s_red = Hammond
                               else: ### Proposition 2
                                   y = a[k]
                                   while Delta[y] < 2:
                                       y = y + 1
                                   Hammond = HammondTransfer(s_red, y, a[k+1] - 1, a[k+1] - 1, a[k+1])
                                   S = SoustractionListe(Hammond, s_red)
                                   L.append(S)
                                   Hammond = s_red                                
        return L      
   else:
        return FirstConditions(s_green, s_red)                    

# Interface utilisateur avec Streamlit
st.title("Hammond Transfers and Ordinal Inequality Measurement: The Algorithm ")

#Guideline
st.header("Guideline:")
st.markdown(""" The algorithm returns an ordered sequence of Hammond transfers that,
                when applied sequentially, transform the dominated distribution 
                into the dominant distribution. A Hammond transfer is noted 
                in the form of a zero-sum vector. In a vector, a negative number indicates
                a decrease in the number of individuals in a given category. 
                Conversely, a positive number indicates an increase in the number of individuals 
                in a given category. For example, the vector (-1,0,2,-1) represents 
                the Hammond transfer, which consists of transferring an individual from 
                category 1 to category 3, and another individual from category 4 to category 3.""")

# Demander à l'utilisateur d'entrer des distributions
s_red_input = st.text_input("Dominated Distribution:")
s_green_input = st.text_input("Dominant Distribution:")


# Convertir les entrées en listes
if s_green_input and s_red_input:
    s_green_input = re.sub(r'[(]', '', s_green_input)
    s_red_input = re.sub(r'[(]', '', s_red_input)
    s_green_input = re.sub(r'[)]', '', s_green_input)
    s_red_input = re.sub(r'[)]', '', s_red_input)
    
    s_green = [int(x) for x in s_green_input.split(',')]
    s_red = [int(x) for x in s_red_input.split(',')]
    
    result = Algorithm1(s_green, s_red)
    
    
    if len(s_green) != len(s_red):#OK
        st.error("ERROR : The two distributions don't have the same number of categories!")
    elif result == 2:#OK
        st.error("ERROR: The two distributions don't have the same number of individuals!")
    elif result == 3:#OK
        st.error("ERROR : No dominance!")
    elif result == 4:#OK
        st.error("ERROR : There is dominance. However the dominant distribution is inverted with the dominated distribution in the algorithm input!")
    else: 
        for b in range(len(result)):#Transforme les listes en vecteur 
            result[b] = re.sub(r'[[]', '(', str(result[b]))
            result[b] = re.sub(r'[]]', ')', result[b])
        # Transformation et affichage du résultat sans guillemets
        result_str = ", ".join(map(str, result))#Crée une chaîne de caractères sans guillemets
        st.write(f"Result: {result_str}")