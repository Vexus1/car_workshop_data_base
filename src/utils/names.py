import pandas as pd

female_names = pd.read_csv(
    "..\\..\\data\\raw\\female_first_names.csv",
    names=["name", "gender", "number"],
    header=0,
).head(150)
male_names = pd.read_csv(
    "..\\..\\data\\raw\\male_first_names.csv",
    names=["name", "gender", "number"],
    header=0,
).head(150)
names = pd.concat([female_names, male_names]).sort_values(by="number", ascending=False)
names.gender = names.gender.replace({"KOBIETA": "F", "MĘŻCZYZNA": "M"})
names["frequency"] = names.number / names.number.sum()
names = names.drop(columns=["number"])

names.to_csv("..\\..\\data\\names.csv")

female_surnames = pd.read_csv(
    "..\\..\\data\\raw\\female_surnames.csv", names=["surname", "number"], header=0
).head(500)
female_surnames["frequency"] = female_surnames.number / female_surnames.number.sum()
female_surnames = female_surnames.drop(columns=["number"])

female_surnames.to_csv("..\\..\\data\\female_surnames.csv")

male_surnames = pd.read_csv(
    "..\\..\\data\\raw\\male_surnames.csv", names=["surname", "number"], header=0
).head(500)
male_surnames["frequency"] = male_surnames.number / male_surnames.number.sum()
male_surnames = male_surnames.drop(columns=["number"])

male_surnames.to_csv("..\\..\\data\\male_surnames.csv")
