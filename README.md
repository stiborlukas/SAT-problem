# Peaceably Co-existing Armies of Queens

## Definice Problému

V úloze „Armies of queens“ je za úkol umístit na šachovnici dvě stejně velké armády černých (B) a bílých (W) královen tak, aby bílé královny neútočily na černé královny (a nutně naopak), a najít maximální velikost těchto dvou armád.

### 1\. Parametry Vstupu

  * **N:** Velikost šachovnice ($N \times N$), kde $N \ge 1$.
  * **K:** Požadovaný minimální počet královen **každé barvy**, kde $0 \le K \le N^2$.

### 2\. Rozhodovací Proměnné

Problém je převeden na splnitelnost (SAT) s následujícími boolovskými proměnnými:

  * **$W_{i,j}$:** Pravda, pokud je **bílá královna** umístěna na pozici $(i, j)$, kde $i, j \in \{0, \dots, N-1\}$.
  * **$B_{i,j}$:** Pravda, pokud je **černá královna** umístěna na pozici $(i, j)$, kde $i, j \in \{0, \dots, N-1\}$.

**Celkový počet proměnných:** $2 \cdot N^2$.

### 3\. Constrainty (Omezení)

Pro nalezení řešení musí být splněny tři hlavní skupiny omezení (klauzule):

1.  **Exkluzivita pozice:** Na jedno pole může být umístěna **maximálně jedna** královna (jakékoliv barvy).
2.  **Bezpečné umístění (No Attack):** Žádná bílá královna nesmí napadat žádnou černou královnu.
3.  **Kardinalita (Počet královen):** Musí být umístěno **alespoň $K$** bílých královen a **alespoň $K$** černých královen.

-----

## Popis Kódování do CNF

Všechna omezení jsou převedena na Konjunktivní Normální Formu (CNF) pro SAT solver v souladu s formátem **DIMACS**.

### Proměnné

Proměnné jsou kódovány celými čísly (literály):

  * **Bílé královny ($W_{i,j}$):** Indexovány od $1$ do $N^2$.
      * $W_{i,j} \rightarrow i \cdot N + j + 1$
  * **Černé královny ($B_{i,j}$):** Indexovány od $N^2 + 1$ do $2N^2$.
      * $B_{i,j} \rightarrow N^2 + i \cdot N + j + 1$

### Kódování Constraintů

#### 1\. Exkluzivita pozice

Pro každé pole $(i, j)$ nesmí být pravdivé $W_{i,j}$ a $B_{i,j}$ současně.

  * **Logická formule:** $\neg (W_{i,j} \wedge B_{i,j})$
  * **CNF klauzule:** $(\neg W_{i,j} \vee \neg B_{i,j})$
  * **Počet klauzulí:** $N^2$

#### 2\. Bezpečné umístění

Pro každou dvojici polí $(i_1, j_1)$ a $(i_2, j_2)$, pokud se napadají (funkce `attacks` v kódu), nesmí být na prvním bílá královna a na druhém černá královna.

  * **Logická formule:** $\neg (W_{i_1, j_1} \wedge B_{i_2, j_2})$
  * **CNF klauzule:** $(\neg W_{i_1, j_1} \vee \neg B_{i_2, j_2})$
  * **Počet klauzulí:** Záleží na $N$; v nejhorším případě blížící se $2 \cdot N^2 \cdot (N^2 - 1)$.

#### 3\. Kardinalita (alespoň K)

Používá se **kombinatorické kódování** pro vynucení podmínky **"alespoň $K$ královen je umístěno"**. To je ekvivalentní podmínce **"nejvýše $N^2 - K$ polí je neobsazených"**.

Definujeme $M = N^2 - K + 1$. Pro každou kombinaci $M$ pozic musí být **alespoň jedna** z těchto pozic obsazena.

  * **CNF klauzule (pro bílé W):** Pro každou kombinaci $M$ pozic $C$:
    $$(\bigvee_{(i, j) \in C} W_{i,j})$$
  * **CNF klauzule (pro černé B):** Stejný princip pro $B_{i,j}$.
  * **Počet klauzulí:** $\mathbf{2 \cdot \binom{N^2}{N^2 - K + 1}}$ (dvě sady: pro W a pro B).

-----

## Uživatelská dokumentace

### Spuštění

Skript vyžaduje zadání instance jedním ze dvou způsobů:

  * **Načtení instance ze souboru** pomocí `-i`, **NEBO**
  * **Ruční specifikace parametrů** pomocí `-n` a `-k`.

Tyto metody nelze kombinovat.

### Základní Použití

```bash
python3 queens.py [-h] [-i INPUT] [-n BOARD_SIZE] [-k NUM_QUEENS] \
                  [-o OUTPUT] [-s SOLVER] [-v {0,1}] [--quiet]
```

### Command-line Options

#### Vstup / Specifikace instance

  * `-i INPUT`, `--input INPUT`: Cesta k souboru s instancí. **Nelze kombinovat s `-n` nebo `-k`.**
  * `-n BOARD_SIZE`, `--board-size BOARD_SIZE`: Velikost šachovnice ($N \times N$). **Musí být použito s `-k`.**
  * `-k NUM_QUEENS`, `--num-queens NUM_QUEENS`: Počet královen každé barvy ($K$). **Musí být použito s `-n`.**

#### Konfigurace výstupu a řešiče

  * `-o OUTPUT`, `--output OUTPUT`: Výstupní soubor pro DIMACS CNF formuli. *Výchozí: `formula.cnf`*
  * `-s SOLVER`, `--solver SOLVER`: SAT řešič k použití. *Výchozí: `glucose-syrup`*
  * `-v {0,1}`, `--verb {0,1}`: Úroveň verbosity SAT řešiče (0 = tichý, 1 = podrobný).
  * `--quiet`: Potlačí verbosity kódování a ostatní výpisy skriptu. (*Výchozí: Verbose*)
  * `-h`, `--help`: Zobrazí nápovědu.

### Formát Vstupu (`-i`)

Vstupní soubor obsahuje dva řádky:

1.  **$N$** (celé číslo, velikost desky $N \times N$)
2.  **$K$** (celé číslo, požadovaný počet královen každé barvy)

<!-- end list -->

```
3
1
```

### Formát Výstupu

Skript vytvoří soubor `formula.cnf` a vypíše výsledek na standardní výstup:

  * **Header:** Označení, zda je problém **SATISFIABLE** (splnitelný) nebo **UNSATISFIABLE** (nesplnitelný).
  * **Sumarizace:** Počet bílých a černých královen nalezených v modelu.
  * **Board layout:** Grafická reprezentace řešení (modelu): `W` (bílá), `B` (černá), `.` (prázdné pole).
  * **TIMING SUMMARY:** Časy pro kódování, řešení a celkový čas.

-----

## Popis Přiložených Instancí

Pro demonstraci a testování jsou přiloženy následující příklady:

  * `3x1-SAT.in`: Malá, snadno analyzovatelná instance, pro kterou **existuje** řešení. ($N=3, K=1$)
  * `3x3-UNSAT.in`: Malá instance, pro kterou řešení **neexistuje**. ($N=3, K=3$)
  * `6x4-SAT.in`: Větší instance, pro kterou existuje řešení, s delší dobou běhu. ($N=6, K=4$)
  * `8x3-SAT.in`: Větší instance, pro kterou existuje řešení, s delší dobou běhu. ($N=8, K=3$)

-----

## Experimenty

**22. 11. 2025 16:32** \
**CPU:** Intel(R) Core(TM) i5-10300H CPU @ 2.50GHz \
**RAM:** 15Gi \
**Systém:** Fedora Linux, Glucose-syrup 4.2.1


### SAT/UNSAT

| n \ k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|
| 1     |UNSAT|-|-|-|-|-|-|-|
| 2     |UNSAT|UNSAT|-|-|-|-|-|-|
| 3     |SAT|UNSAT|UNSAT|-|-|-|-|-|
| 4     |SAT|SAT|UNSAT|UNSAT|-|-|-|-|
| 5     |SAT|SAT|SAT|SAT|UNSAT|-|-|-|
| 6     |SAT|SAT|SAT|SAT|SAT|UNSAT|-|-|
| 7     |SAT|SAT|SAT|SAT|???|???|???|-|
| 8     |SAT|SAT|SAT|???|???|???|???|???|

<br>

### Total clauses

| n \ k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|
| 1     |1|-|-|-|-|-|-|-|
| 2     |18|24|-|-|-|-|-|-|
| 3     |67|83|137|-|-|-|-|-|
| 4     |170|200|408|1288|-|-|-|-|
| 5     |347|395|945|4945|25645|-|-|-|
| 6     |618|688|1876|14896|118426|754600|-|-|
| 7     |1003|1099|3353|37849|424753|3814769|27968633|-|
| 8     |1522|1648|5552|84848|1272272|15250544|???|???|

<br>

### Total time (s)

| n \ k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|
| 1     |0,002|-|-|-|-|-|-|-|
| 2     |0,002|0,004|-|-|-|-|-|-|
| 3     |0,004|0,004|0,004|-|-|-|-|-|
| 4     |0,005|0,005|0,011|0,034|-|-|-|-|
| 5     |0,005|0,007|0,034|0,444|8,129|-|-|-|
| 6     |0,006|0,015|0,217|5,145|187,546|8736,543|-|-|
| 7     |0,008|0,043|3,294|245,465|???|???|???|-|
| 8     |0,011|0,115|26,234|???|???|???|???|???|

**Legenda:**

  * **Řádky =** velikost desky $N$, **sloupce =** počet královen $K$.
  * **SAT/UNSAT:** splnitelnost instance.
  * **Total clauses:** celkový počet klauzulí v CNF.
  * **Total time:** celkový čas běhu (kódování + řešení) v sekundách.
  * **???** znamená neměřeno/příliš dlouhý běh.