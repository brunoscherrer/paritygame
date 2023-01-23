
On considère un jeu de parité G joué par ADAM et EVE, avec fonction de priorité p:X -> [0,1,...,d]. Lorsque la priorité maximale qui est visitée un nombre infini de fois est nulle, on dira que la partie est nulle.

Pour tout jeu de parité G, on peut construire un jeu de cout moyen \hat{G} ayant la même dynamique et une fonction de cout:
- g(x)=(-(N+1))^p(x) si p(x)>0
- g(x)=0
  
Pour tout jeu G, on note G_{>=k} une copie de G dans laquelle les priorités <k sont remplacées par la priorité 0.

Hypothèse H_{j}(G,mu,nu):
Dans le jeu G, pour tout état initial,
- La politique mu d'EVE permet d'avoir une parité strictement inférieure à j+1
- La politique nu d'ADAM permet d'avoir une parité strictement inférieure à j
ou (de manière équivalente):
Le jeu G_{>=j} a pour valeur 0.

Au début H_{d+1}(G,mu,nu) est vraie pour tout (mu,nu).

Supposons que H_{j}(G,mu,nu) est vraie. On suppose que j est pair, càd de la forme 2k (le cas 2k+1 est analogue).

Considérons le jeu G_0=G_{>=2k}. Pour tout nu', la trajectoire induite par (mu,nu') va cycler indéfiniment vers des états de G_0 de priorité nulle. Soit A cet ensemble d'états (on peut le calculer avec n^2+n étapes de VI).

Considérons le jeu G_1=G_{>=2k-1} (dans lequel on rajoute par rapport à G_0 les priorités 2k-1). On peut résoudre le jeu  G_2=G_1 \cup A (c'est un jeu avec 2 priorité). Soit B l'ensemble des états gagnés par ADAM dans G_2.

Si B est l'ensemble vide, alors on sait que EVE a une politique telle que la meilleure priorité impaire est strictement plus petite que 2k-1. Calculons la meilleur politique nu' pour ADAM. Autrement dit, H_{k-1}(G,mu',nu'} est vraie (donc on peut itérer avec j-1 avec G_0).

Si B est non vide, on sait que dans G_0, ADAM peut gagner sur C=1-Attr(B). On considère alors le jeu G_3=G\C.

Si le jeu G_3 est vide, alors c'est fini (on sait que ADAM gagne le jeu G_0 pour tout état initial).

Si le jeu G_3 est non vide, on peut tester si H_{2k}(G_3) est vraie en calculant la politique optimale de EVE face à la politique nu de ADAM. Si H_{2k}(G_3} n'est pas vraie, on sait que ADAM gagne le jeu G_0 avec priorité 2k-1. Sinon on itère comme au dessus avec G_3 au lieu de G_0. A chaque étape, soit on termine, soit on réduit la taille du jeu considéré. Cela dure donc au plus n iterations.

A chaque étape de la procédure ci-dessus, la priorité considérée diminue, donc on a au plus d étapes.

Au final, on a au plus O(d n^4) étapes de VI, soit une complexité de O(d n^5 m). 



PS: je pense qu'il est possible d'utiliser le même genre d'idées pour un jeu de cout moyen  (avec une technique de scaling, on devrait pouvoir mettre à jour la valeur d'un jeu dont on change la récompense R par R+delta avec 0<=delta<=1).