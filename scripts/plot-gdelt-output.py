from argparse import ArgumentParser

import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    df = pd.read_csv(args.filename)

    plt.figure()
    plt.plot(df["corpus_score"], df["sentiment_salience"], "k+")
    plt.show(block=False)

    cond = df["corpus_score"] > 0.02
    cond &= df["sentiment_salience"] > 0.3
    print(cond.sum())
