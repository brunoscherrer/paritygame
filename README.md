# paritygame
description d'un algo polynomial pour le jeu de parité

On considère un jeu de parité avec p:X -> N, avec possible priorité nulle (neutre).
On peut regarder ce jeu comme un jeu de cout moyen avec cout
g(x)=(-N)^p(x).

Pour tout jeu G, on note G_{>=k} une copie de G dans laquelle les priorités <k sont remplacées par 0.

Hypothèse H_{2k}(G):
Dans le jeu G,
- MAX a une politique telle que la meilleure priorité impaire est plus petite que 2k+1.
- MIN a une politique telle que la meilleure priorité paire est plus petite que 2k.

Hypothèse H_{2k-1}(G):
Dans le jeu G,
- MIN a une politique telle que la meilleure priorité paire est plus petite que 2k.
- MAX a une politique telle que la meilleure priorité impaire est plus petite que 2k-1.

Au début H_{pmax+1} est évidemment vraie (pour toute politique)

Supposons que H_{2k}(G) est vraie (le cas 2k+1 est analogue). Considérons un jeu G_0=G_{>=2k}. Il existe une politique nu pour MIN telle que pour toute politique de MAX, la valeur du jeu est 0; ainsi, la trajectoire va cycler indéfiniment vers des états de G de priorité nulle. On peut calculer nu et cet ensemble A d'états avec O(n^3) iterations de VI (cf. Zwick et Paterson) (les états de A sont pour lesquels la valeur T^{4n^3}0(x)=0).

On peut maintenant considérer le jeu G_1=G_{>=2k-1} (dans lequel on rajoute par rapport à G_0 les priorités 2k-1). On peut résoudre G_1 restreint à A (c'est équivalent à un jeu de cout moyen avec valeurs {0 -1}). Soit B l'ensemble des états gagnés par MIN.

Si B est l'ensemble vide, alors on sait que MAX a une politique telle que la meilleure priorité impaire est plus petite que 2k-1. Autrement dit, H_{k-1}(G} est vraie (donc on peut itérer avec 2k-1 avec G_0).

Si B est non vide, on sait que dans G_0, MIN peut gagner sur C=1-Attr(B). On considère alors le jeu G_2=G\C.

Si le jeu G_2 est vide, alors c'est fini (on sait que MIN gagne le jeu G_0 pour tout état initial).

Si le jeu G_2 est non vide, on peut tester si H_{2k}(G_2) est vraie en calculant la politique optimale de MAX face à la politique nu de MIN. Si H_{2k}(G_2} n'est pas vraie, on sait que MIN gagne le jeu G_0 avec priorité 2k-1. Sinon on itère comme au dessus avec G_2 au lieu de G_0. A chaque étape, soit on termine, soit on réduit la taille du jeu considéré. Cela dure donc au plus n iterations.

A chaque étape de la procédure ci-dessus, la priorité considérée diminue, donc on a au plus d étapes.

Au final, on a au plus O(d n^4) étapes de VI, soit une complexité de O(d n^5 m). 



PS: je pense qu'il est possible d'utiliser le même genre d'idées pour un jeu de cout moyen  (avec une technique de scaling, on devrait pouvoir mettre à jour la valeur d'un jeu dont on change la récompense R par R+delta avec 0<=delta<=1.