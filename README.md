Komandinis darbas, sveikatos indekso analizė ✔

⫸ Visos šalys

![I_img_3.png](sveikatos_analize%2FI_img_3.png)

______________________________________________________________________
⫸ Baltijos ir Skandinavijos šalys

![I_img_2.png](sveikatos_analize%2FI_img_2.png)

______________________________________________________________________
⫸ Baltijos šalys

![I_img_1.png](sveikatos_analize%2FI_img_1.png)


______________________________________________________________________
Gyventojų sveikatos duomenų analizė (duomenų paruošimas mašininiam mokymui, mašininio mokymo modelių pasirinkimas,
modelio mokymas ir įvertinimas , hiperparametrų derinimas ir modelio optimizavimas).

Naudojant LinearRegression:

![II_LinearRegression.png](sveikatos_analize%2FII_LinearRegression.png)

Modelio metrikų įvertinimas:



⫸ MSE:  0.0011604802650220872

⫸ R2:  0.9496641160143532

⫸ RMSE:  0.034065822535528

⫸ Cross Validation Scores:  [0.94966412 0.93233879 0.93261997 0.94692378 0.92734106]

⫸ Average CV Score:  0.9377775434590931

⫸ Number of CV Scores used in Average:  5

______________________________________________________________________

Naudojant K-means:

![II_K-means.png](sveikatos_analize%2FII_K-means.png)

Modelio metrikų įvertinimas:

⫸ MSE 0.021261494126798057

⫸ R2 0.07778173055993431


Geriausių klasterių skaičius nustatytas naudojant Silhouette score ir Elbow grafiką:

![II_Elbow.png](sveikatos_analize%2FII_Elbow.png)

⫸ The best silhouette score is with 3 clusters

2 clusters silhouette score: 0.63

3 clusters silhouette score: 0.59

4 clusters silhouette score: 0.57

5 clusters silhouette score: 0.56

6 clusters silhouette score: 0.55

7 clusters silhouette score: 0.55

8 clusters silhouette score: 0.54

9 clusters silhouette score: 0.54

10 clusters silhouette score: 0.54



______________________________________________________________________

Naudojant RandomForest:

[II_RandomForest.py](sveikatos_analize%2FII_RandomForest.py)

Modelio metrikų įvertinimas:

⫸ Best hyperparameters: {'max_depth': None, 'n_estimators': 300}

⫸ Best result: -0.006810983113629083

______________________________________________________________________

Naudojant LogisticRegression:

![II_ROCcurve.png](sveikatos_analize%2FII_ROCcurve.png)

Modelio metrikų įvertinimas:

⫸ AUC: 0.9805760953537138

______________________________________________________________________

Naudojant DBSCAN:

[II_DBSCAN.py](sveikatos_analize%2FII_DBSCAN.py)

