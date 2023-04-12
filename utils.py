def get_digit_df(df, GIAI):
    import pandas as pd

    if df.shape[0] is 0:
        return

    df = df[['Nam', 'Thu', GIAI]].reset_index()
    num_of_turns = len(df[GIAI][0].split())
    num_of_digits = len(df[GIAI][0].split()[0])

    def extract_turns(df):

        df_turn = pd.concat([df, df[GIAI].str.split(
            expand=True)], axis=1).drop(columns=[GIAI])
        tmp = df_turn[['Nam', 'Thu', 0]].rename(columns={0: GIAI})

        for i in range(1, num_of_turns):
            tmp = pd.concat(
                [tmp, df_turn[['Nam', 'Thu', i]].rename(columns={i: GIAI})], axis=0)

        return tmp.reset_index()

    def extract_digits(df):

        for i in range(num_of_digits):
            df[f'digit_{i+1}'] = df[GIAI].apply(lambda s: list(s)[i])

        return df

    df = extract_turns(df)
    df = extract_digits(df)

    return df.drop(columns=['index'])


def chi2_test(hist, msg, SIGNIFICANT_LEVEL):
    from scipy.stats import chisquare
    stats, pvalue = chisquare(hist, axis=0)

    if pvalue < SIGNIFICANT_LEVEL:
        print(
            f"{msg}: Statistics {stats:.3f}, Pvalue {pvalue:.5f}, indicates Not Uniformly Distributed")
    else:
        print(
            f"{msg}: Statistics {stats:.3f}, Pvalue {pvalue:.5f}, not enough evidence")
