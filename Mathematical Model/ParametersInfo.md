# Parameters Info
This contains information detailing how to read/change the **`parameters.xlsx`** file. One might only understand this section fully if the paper is read.

## Explaining Values in Single Sheet
1. **`g1_percentage`**: Between 0 and 1. The proportion of group 1 individuals that enters the company at each time step $t$. It also represents the proportion of individuals in group 1 at the lowermost level at $t=0$.
2. **`g1_assertiveness`**:  Both values in list are between 0 and 1. A list with two values which we denote mathematically as [$\mu_{a}(1), \mu_{\alpha}(1)($]. The first value in the list represents the mean internal assertiveness of group 1, and the second value represents the mean perceived assertiveness of group 1.
3. **`g2_assertiveness`**:  A list with two values which we denote mathematically as [$\mu_a(2), \mu_{\alpha}(2)($]. The first value in the list represents the mean internal assertiveness of group 2, and the second value represents the mean perceived assertiveness of group 2.
4. **`Beta`**: Between 0 and 1. Represents $\beta$ in the paper. The importance of assertiveness to the person who does the hiring.
5. **`sd`**: A tuple with two values. The first value represents the standard deviation for the normal distributions that generates the internal and perceived assertiveness for individuals in group 1.  The second value similarly represents the standard deviation for the normal distributions that generates the internal and perceived assertiveness for individuals in group 2.
6. **`num_start`**: An integer. Represents the number of individuals in at the lowest (sub)level ($L_0$) at $t=0$.
7. **`num_incoming`**: An integer. Represents the numb of individuals that enter the company at $L_0$ each time step $t$.
8. **`group_parameters`: A list of lists of a length of 3. This parameter prefills the company at each sublevel so that the company is (or isn't) empty at $t=0$. We explain this parameter more in detail at the bottom.
9. **`num_levels`**: An integer. Represents the number of levels in the company. Our company will start at $L_0$, so 3 levels indicates 7 sublevels as there are two sublevels within each level. This means the sublevels are as follows: $L_0$, $C_1$, $L_1$, $C_1$, $L_2$, $C_2$, $L_3$.
10. **$t$**: An integer. Represents number of a time steps in a single simulation. Default is 100.
11. **`Simulations`**: An integer. Number of simulations for each row in a sheet, or for a given set of parameters. Default is 50.
12. **`name_file`**: The name of the file in which the results for the set of parameters is stored.

### `group_parameters`
Each 3-item list in the list sets the parameter values for that sub-level.
1. *`*sublevel_index`**: The first item in the sublist is an integer indicating the index of the sublevel. The order of the sublist in the list helps determines the index.
2. **`number_of_individuals`**: The second item in the sublist is an integer indicating the number of individuals at that sublevel.
3. **`proportion_of_g1_individuals`**: The third item in the list is a proportion indicating the proportion of group 1 individuals at that sublevel. Default is 0.5.

Below is the mapping of the index to the sublevel assuming `num_levels=3`: 

0: (not present as it's determined by `num_start` and `g1_percentage`)

1: $C_0$

2: $L_1$

3: $C_1$

4: $L_2$

5: $C_2$

6: $L_3$



## Explaining Sheet Names
Each sheet name is ultimately made up of two parts:
1. The parameter(s) of interest in this specific sheet
2. The preset `group_parameters` of interest in this specific sheet

### Parameters of Interest
1. **a**: If the sheet's title contains **a** (and no other parameter), this means we examine different combinations of values of $\mu_a(1)$ and $\mu_a(2)$ in each row of this sheet.
2. **alpha**: If the sheet's title contains **alpha** (and no other parameter), this means we examine different combinations of values of $\mu_{\alpha}(1)$ and $\mu_{\alpha}(2)$ in each row of this sheet.
3. **a_alpha**: If the sheet's title contains **a_alpha**, this means we examine different combinations of values of $\mu_{a}(1)$, $\mu_{a}(2)$, $\mu_{\alpha}(1)$ and $\mu_{\alpha}(2)$ in each row of this sheet.
4. **beta**: If the sheet's title contains **beta** (and no other parameter), this means we examine different values of $\beta$ in each row of this sheet.

### The Preset `group_parameters`
1. **If no word follows the parameter(s) of interest in the name**, this means that `number_of_individuals` is equivalent across all sublevels at $t=0$ and equivalent across different sets of parameters.
2. **If *diff_constant_prefilled* follows the parameter(s) of interest**, this means that  `number_of_individuals` is equivalent across all sublevels at $t=0$ within a given set of parameters, but it varies for each set of parameters (the value of `number_of_individuals` differs between rows in a single sheet).
3. **If *diff_var_prefilled* follows the parameter(s) of interest**, this means that  `number_of_individuals` is different across all sublevels at $t=0$ within a given set of parameters *and* it varies for each set of parameters (value of `number_of_individuals` differs between rows in a single sheet).
