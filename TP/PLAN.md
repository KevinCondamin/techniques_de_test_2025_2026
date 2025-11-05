# Plan de test

## Tests unitaires

1. Test du calcul de triangulation avec un `PointSet` vide pour vérifier si le service renvoie un élément vide.
2. Test du calcul de triangulation avec un `PointSet` inexistant pour vérifier si le service renvoie une erreur.
3. Test du calcul de triangulation avec un `PointSet` contenant deux points pour vérifier si le service renvoie un élément vide.
4. Test du calcul de triangulation avec un `PointSet` contenant trois points ou plus pour vérifier si le service renvoie ce qu'on veut.
5. Test du calcul de triangulation avec un `PointSet` invalide pour vérifier si le service renvoie une erreur.
6. Test de la représentation binaire de `Triangles` pour un `Triangles` erroné.
7. Test de la représentation binaire de `Triangles` pour un `Triangles` correct.
8. Test de la représentation binaire de `PointSet` pour un `PointSet` erroné.
9. Test de la représentation binaire de `PointSet` pour un `PointSet` correct.
10. Test de la représentation du type `Triangles` en partant d'une représentation binaire erronée.
11. Test de la représentation du type `Triangles` en partant d'une représentation binaire correcte.
12. Test de la représentation du type `PointSet` en partant d'une représentation binaire erronée.
13. Test de la représentation du type `PointSet` en partant d'une représentation binaire correcte.
14. [**Cas limite**] Test du calcul de triangulation avec un `PointSet` contenant des points colinéaires pour vérifier si le service renvoie une représentation correcte de `Triangles`.

## Tests de performance

1. Test de la vitesse de calcul de triangulation avec un `PointSet` contenant 3 points.
2. Test de la vitesse de calcul de triangulation avec un `PointSet` contenant 50 points.
3. Test de la vitesse de la conversion de `PointSet` en binaire.
4. Test de la vitesse de la conversion de binaire en `PointSet`.
5. Test de la vitesse de la conversion de `Triangles` en binaire.
6. Test de la vitesse de la conversion de binaire en `Triangles`.

## Mise en place de ces tests

Pour les tests de triangulation avec ou sans erreur, il y aura, pour certains cas, une story à réaliser.

Pour les tests de performance, il faudra calculer le temps que cela prend entre le moment où on fait l'appel et le moment où la fonction nous retourne le résultat. Il faudra donc utiliser un outil de Python permettant de mesurer le temps d'exécution d'une portion de code.

Etant donné que nous n'avons pas le service `PointSetManager` d'implémenté, ni la base de données, nous allons devoir créer des mocks de ces deux services.