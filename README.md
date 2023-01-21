# paritygame
description d'un algo polynomial pour le jeu de parité

On considère un jeu de parité avec p:X -> N, avec possible priorité nulle (neutre).
On peut regarder ce jeu comme un jeu de cout moyen avec cout
g(x)=(-N)^p(x).


Hypothèse H_{2k}(G)
Dans le jeu G,
MAX a une politique telle que la meilleure priorité impaire est plus petite que 2k+1.
MIN a une politique telle que la meilleure priorité paire est plus petite que 2k.

Hypothèse H_{2k-1}(G)
Dans le jeu G,
MIN a une politique telle que la meilleure priorité paire est plus petite que 2k.
MAX a une politique telle que la meilleure priorité impaire est plus petite que 2k-1.

Au début H_{pmax+1} est vraie.

Considérons un jeu G où on a des priorités >=2k, où l'on remplace toutes les priorités <2k sont egales à 0. Supposons que H_{2k}(G) est vraie: il existe une politique pour MIN telle que pour toute politique de MAX, la trajectoire va cycler vers des états de G de priorité nulle. On peut calculer cet ensemble A d'états avec 4n^3 iterations de VI (cf. Zwick et Paterson).

On peut maintenant considérer le jeu G' dans lequel on rajoute par rapport à G les priorités 2k-1. On peut résoudre G' restreint à A (c'est équivalent à un jeu de cout moyen avec valeurs 0 -1). Soit B l'ensemble des états gagnés par MIN.

Si B est l'ensemble vide, alors on sait que MAX a une politique telle que la meilleure priorité impaire est plus petite que 2k-1. Autrement dit, H_{k-1} est vraie (donc on peut itérer).

Si B est non vide, on sait que dans G, MIN peut gagner sur C=1-Attr(B). On considère alors le jeu G''=G\C.

Si le jeu G'' est vide, alors c'est fini (on sait que MIN gagne le jeu G pour tout état initial).

Si le jeu G'' est non vide, on sait que H_{2k}(G'') est vraie. Donc on itère comme au dessus avec G''.



