# A Causal View for Item-level Effect of Recommendation on User Preference

## Dataset

1. Download the MIND dataset from [https://msnews.github.io/](https://msnews.github.io/).
2. Unzip the files `MINDlarge_train.zip` and `MINDlarge_dev.zip`.
3. Put the folders `MINDlarge_train` and `MINDlarge_dev` into `data/mind`.
4. Run `chmod 777 prepare_data.sh` and `./prepare_data.sh` in `data/mind`.

## Examples to run
Eliminating the time confounder:
1. `cd debias_time`.
2. `python debias_time.py --s_model=sam --s_len=1000`.
  * `--s_model`: The stratification model.
    * `direct`: The direct estimation without stratification.
    * `rs`: Randomly stratify the samples.
    * `strat`: Stratification with our proposed approximation strategy.
    * `sam`: Our method (including both stratification and matching) with approximation strategies.
  * `--s_len`: The size of each subgroup.

Eliminating the user feature confounder:
1. `cd debias_user`.
2. Eliminating the user click rate bias: `python debias_urate.py --m_model=sam --s_len=1000`.
  * `--m_model`: The matching model.
    * `direct`: The direct estimation without matching.
    * `rm`: Randomly match the samples.
    * `matwdr, matwdvr, matwde`: Matching with $d^\mbox{r}$, $d^\mbox{vr}$ and $d^\mbox{e}$, respectively.
    * `mat`: Matching with $d'$.
    * `sam`: Our method (including both stratification and matching) with approximation strategies.
  * `--s_len`: The size of each subgroup.
3. Eliminating the bias of user click rates for category g: `python debias_ugrate.py --m_model=sam --s_len=1000`.
    * The meanings of the parameters are the same as above.

Thanks for using our code!
